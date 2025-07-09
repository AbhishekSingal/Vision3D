import numpy as np
import pyvista as pv
from pyvistaqt import QtInteractor
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QPushButton, QVBoxLayout, 
    QWidget, QLabel, QHBoxLayout, QLineEdit, QFileDialog, QSplitter
)
from PyQt5.QtCore import QTimer
import trimesh
import os
import json
from datetime import datetime
from PyQt5.QtWidgets import QDialog, QInputDialog, QScrollArea, QDialogButtonBox
from PyQt5.QtWidgets import QDockWidget, QTreeWidget, QTreeWidgetItem, QLabel, QVBoxLayout, QWidget
from PyQt5.QtWidgets import QDialog, QVBoxLayout, QListWidget, QLabel
from PyQt5.QtCore import Qt,pyqtSignal

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QLabel, QSplitter, QDialog, QListWidget,
    QTabWidget, QDockWidget, QMenuBar, QMenu, QAction
)

import Styles.colors as cl

class Point:
    def __init__(self, x: float, y: float, z: float, selected: bool = False):
        self.x = x
        self.y = y
        self.z = z
        self.selected = selected
        self._visible = True

    def toList(self):
        return [self.x, self.y, self.z]

    def toNumpy(self):
        return np.array([self.x, self.y, self.z])

    def distanceTo(self, other):
        return np.linalg.norm(self.toNumpy() - other.toNumpy())

    def __repr__(self):
        return f"Point({self.x}, {self.y}, {self.z}, selected={self.selected})"
    
    def toggleVisibility(self):
        self._visible = not self._visible

class Line:
    def __init__(self, point1: Point, point2: Point):
        self.point1 = point1
        self.point2 = point2
        self.selected = False
        self._visible = True

    def length(self):
        return self.point1.distanceTo(self.point2)

    def directionVector(self):
        return self.point2.toNumpy() - self.point1.toNumpy()

    def toVtkLine(self):
        return pv.Line(self.point1.toNumpy(), self.point2.toNumpy())

    def __repr__(self):
        return f"Line({self.point1} -> {self.point2})"

class Surface:
    def __init__(self, points: list):
        self.points = points
        self.selected = False
        self._visible = True
        self._mesh = None
        self._updateMesh()

    def _updateMesh(self):
        pointsArray = np.array([p.toNumpy() for p in self.points])
        if len(pointsArray) >= 3:
            self._mesh = pv.PolyData(pointsArray).delaunay_2d()
            self._mesh = self._mesh.subdivide(nsub=3, subfilter="linear")
            self._mesh = self._mesh.smooth(n_iter=100, relaxation_factor=0.1)
        else:
            self._mesh = None

    def getMesh(self):
        return self._mesh

    def addPoint(self, point: Point):
        self.points.append(point)
        self._updateMesh()
    


    def __repr__(self):
        return f"Surface({len(self.points)} points)"

class Sensor(Point):
    def __init__(self, x: float, y: float, z: float, selected: bool = False):
        super().__init__(x, y, z, selected)
        self.value = 0.0  # Additional sensor-specific attribute
        self.history = []  # Store historical values

    def updateValue(self, newValue):
        self.history.append(self.value)
        self.value = newValue

    def __repr__(self):
        return f"Sensor({self.x}, {self.y}, {self.z}, value={self.value})"
    

class Renderer(QWidget):
    pointSelectionChanged = pyqtSignal(int, bool)
    sensorSelectionChanged = pyqtSignal(int, bool)
    def __init__(self):
        super().__init__()
        
        # Data structures using our new classes
        self.points: list[Point] = []
        self.lines: list[Line] = []
        self.surfaces: list[Surface] = []
        self.sensors: list[Sensor] = []
        
        # Selection tracking
        self.selectedPoints: list[int] = []      # Indices of selected points
        self.selectedLines: list[int] = []       # Indices of selected lines
        self.selectedSurfaces: list[int] = []    # Indices of selected surfaces
        self.selectedSensor: int = -1            # Index of selected sensor
        

        # UI and 3D setup
        self.setupUi()
        self.setupVisualProperties()
        
        # Animation
        self.vibrationTimer = QTimer()
        self.vibrationTimer.timeout.connect(self.animateSurface)
        self.vibrationPhase = 0.0
        

        # Vibrations
        self.vib_amplitude = 0.05
        self.vib_frequency = 2
        self.vib_x_inf = 0.5
        self.vib_y_inf = 0.5
        self.vib_speed = 50
        
        # File management
        self.currentFilePath = None

    def deletePoint(self, idx: int,updatePlot = True):
        """Delete a point and all connected lines/surfaces"""
        if idx < 0 or idx >= len(self.points):
            return False

        # Remove lines connected to this point
        self.lines = [
            line for line in self.lines
            if line.point1 != self.points[idx] and line.point2 != self.points[idx]
        ]

        # Remove surfaces containing this point
        self.surfaces = [
            surface for surface in self.surfaces
            if self.points[idx] not in surface.points
        ]

        # Remove the point
        del self.points[idx]

        # Update selections
        self.selectedPoints = [i if i < idx else i - 1 for i in self.selectedPoints if i != idx]
        self.selectedLines.clear()
        self.selectedSurfaces.clear()
        if updatePlot:
            self.updatePlot()
        return True

    def deleteLine(self, idx: int):
        """Delete a line by index"""
        if idx < 0 or idx >= len(self.lines):
            return False
        del self.lines[idx]
        self.selectedLines = [i for i in self.selectedLines if i != idx]
        self.updatePlot()
        return True

    def deleteSensor(self, idx: int):
        """Delete a sensor by index"""
        if idx < 0 or idx >= len(self.sensors):
            return False
        del self.sensors[idx]
        if self.selectedSensor == idx:
            self.selectedSensor = -1
        elif self.selectedSensor > idx:
            self.selectedSensor -= 1
        self.updatePlot()
        return True
    
    def setupUi(self):
        """Initialize the 3D viewer and UI layout"""
        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Initialize the 3D plotter
        self.plotter = QtInteractor(self)
        self.plotter.set_background(cl.SYS_BG4)
        self.plotter.enable_terrain_style()
        self.plotter.add_axes(interactive=True)
        
        # Enable point picking
        self.plotter.enable_point_picking(
            callback=self.handlePick,
            use_mesh=False,
            show_point=True,
            tolerance=1,
            left_clicking=True,
            show_message=False,
        )
        
        layout.addWidget(self.plotter, 1)
        self.setLayout(layout)

    def setupVisualProperties(self):
        """Configure default visual properties"""
        # Points
        self.pointColor = [255, 0, 0]        # Red
        self.pointSelectedColor = [0, 0, 255]  # Blue
        self.pointSize = 10
        
        # Lines
        self.lineColor = [0, 255, 0]         # Green
        self.lineSelectedColor = [255, 0, 0]  # Red
        self.lineWidth = 3
        
        # Surfaces
        self.surfaceColor = 'lightgreen'
        self.surfaceSelectedColor = 'orange'
        self.surfaceEdgeColor = 'white'
        self.surfaceOpacity = 0.6
        self.showSurfaceEdges = True
        
        # Sensors
        self.sensorColor = [255, 255, 0]     # Yellow
        self.sensorSelectedColor = [0, 255, 0]  # Green
        self.sensorSize = 15

    # ==================== Core Methods ==================== #

    def addPoint(self, x: float, y: float, z: float,update=True):
        """Add a new point to the scene"""
        self.points.append(Point(x, y, z))
        if update:
            self.updatePlot()
    

    def addSensor(self, x: float, y: float, z: float):
        """Add a new sensor to the scene"""
        self.sensors.append(Sensor(x, y, z))
        self.updatePlot()

    def connectPoints(self, idx1: int, idx2: int):
        """Create a line between two points"""
        if idx1 < 0 or idx2 < 0 or idx1 >= len(self.points) or idx2 >= len(self.points):
            return False
        
        # Check if line already exists
        for line in self.lines:
            if (line.point1 == self.points[idx1] and line.point2 == self.points[idx2]) or \
               (line.point1 == self.points[idx2] and line.point2 == self.points[idx1]):
                return False
        
        self.lines.append(Line(self.points[idx1], self.points[idx2]))
        self.updatePlot()
        return True
    
    def connectSelectedPoints(self):
        if len(self.selectedPoints) == 2:
            p1 = self.points[self.selectedPoints[0]]
            p2 = self.points[self.selectedPoints[1]]
            self.lines.append(Line(p1,p2))
            self.updatePlot()

    def drawSurfaceFromSelection(self):
        if len(self.selectedPoints) >= 2:
            ps = []
            for p in self.selectedPoints:
                ps.append(self.points[p])
            surface = Surface(ps)
            self.surfaces.append(surface)
            self.updatePlot()

    def drawMultiplePoints(self,points:list):
        for point in points:
            self.points.append(Point(point[0],point[1],point[2]))
        self.updatePlot()

        

    def createSurface(self, pointIndices: list):
        """Create a surface from selected points"""
        if len(pointIndices) < 3:
            return False
        
        surfacePoints = [self.points[i] for i in pointIndices]
        self.surfaces.append(Surface(surfacePoints))
        self.updatePlot()
        return True

    def updatePlot(self,points_only = False):
        """Update the 3D visualization"""
        if points_only == True:
            self.plotter.remove_actor("points")
        else:
            self.plotter.clear()
        
        # Add points
        if self.points:
            pointCoords = np.array([p.toNumpy() for p in self.points])
            pointColors = np.array([
                self.pointSelectedColor if i in self.selectedPoints else self.pointColor 
                for i in range(len(self.points))
            ])
            
            pointsMesh = pv.PolyData(pointCoords)
            pointsMesh["colors"] = pointColors
            
            self.plotter.add_mesh(
                pointsMesh,
                scalars="colors",
                rgb=True,
                point_size=self.pointSize,
                render_points_as_spheres=True,
                name="points"
            )
        
        if points_only == True:
            return
        
        # Add lines
        for i, line in enumerate(self.lines):
            lineColor = self.lineSelectedColor if i in self.selectedLines else self.lineColor
            self.plotter.add_mesh(
                line.toVtkLine(),
                color=lineColor,
                line_width=self.lineWidth,
                name=f"line_{i}"
            )
        
        # Add surfaces
        for i, surface in enumerate(self.surfaces):
            if surface.getMesh() is not None:
                surfaceColor = self.surfaceSelectedColor if i in self.selectedSurfaces else self.surfaceColor
                self.plotter.add_mesh(
                    surface.getMesh(),
                    color=surfaceColor,
                    opacity=self.surfaceOpacity,
                    show_edges=self.showSurfaceEdges,
                    edge_color=self.surfaceEdgeColor,
                    name=f"surface_{i}",
                    pickable=False
                )
        
        # Add sensors
        if self.sensors:
            sensorCoords = np.array([s.toNumpy() for s in self.sensors])
            sensorColors = np.array([
                self.sensorSelectedColor if i == self.selectedSensor else self.sensorColor
                for i in range(len(self.sensors))
            ])
            
            sensorsMesh = pv.PolyData(sensorCoords)
            sensorsMesh["colors"] = sensorColors
            
            self.plotter.add_mesh(
                sensorsMesh,
                scalars="colors",
                rgb=True,
                point_size=self.sensorSize,
                render_points_as_spheres=True,
                name="sensors"
            )
        # self.plotter.reset_camera()

    # ==================== Selection Methods ==================== #

    def handlePick(self, picked):
        """Handle point picking events"""
        if self.pickSensor(picked):
            return
        self.pickPoint(picked)

    def pickPoint(self, pickedCoords):
        """Select a point near the picked coordinates"""
        if not self.points:
            return False
        
        pointsArray = np.array([p.toNumpy() for p in self.points])
        dists = np.linalg.norm(pointsArray - pickedCoords, axis=1)
        nearestIdx = np.argmin(dists)
        
        if dists[nearestIdx] > self.selectionThreshold():
            return False
        
        if nearestIdx in self.selectedPoints:
            self.selectedPoints.remove(nearestIdx)
            isSelected = False
        else:
            self.selectedPoints.append(nearestIdx)
            isSelected = True
        
        self.updatePlot(points_only=True)
        self.pointSelectionChanged.emit(nearestIdx, isSelected)
        return True

    def pickSensor(self, pickedCoords):
        """Select a sensor near the picked coordinates"""
        if not self.sensors:
            return False
        
        sensorsArray = np.array([s.toNumpy() for s in self.sensors])
        dists = np.linalg.norm(sensorsArray - pickedCoords, axis=1)
        nearestIdx = np.argmin(dists)
        
        if dists[nearestIdx] > self.selectionThreshold():
            return False
        
        self.selectedSensor = nearestIdx if self.selectedSensor != nearestIdx else -1
        self.updatePlot()
        return True

    def selectionThreshold(self):
        """Calculate dynamic selection threshold based on point density"""
        if len(self.points) < 2:
            return 0.5
        
        # Calculate average distance between points
        pointsArray = np.array([p.toNumpy() for p in self.points])
        dists = []
        for i in range(len(self.points)):
            for j in range(i+1, len(self.points)):
                dists.append(np.linalg.norm(pointsArray[i] - pointsArray[j]))
        
        return np.mean(dists) * 0.5 if dists else 0.5

    def clearSelection(self):
        """Clear all selections"""
        self.selectedPoints.clear()
        self.selectedLines.clear()
        self.selectedSurfaces.clear()
        self.selectedSensor = -1
        self.updatePlot()

    # ==================== File I/O Methods ==================== #

    def saveModel(self, filePath):
        """Save the current model to a JSON file"""
        if not filePath.endswith('.model'):
            filePath += '.model'

        try:
            modelData = {
                "points": [p.toList() for p in self.points],
                "lines": [
                    [self.points.index(line.point1), self.points.index(line.point2)] 
                    for line in self.lines
                ],
                "surfaces": [
                    [self.points.index(p) for p in surface.points]
                    for surface in self.surfaces
                ],
                "sensors": [s.toList() for s in self.sensors],
                "metadata": {
                    "created": datetime.now().isoformat(),
                    "numPoints": len(self.points),
                    "numLines": len(self.lines),
                    "numSurfaces": len(self.surfaces),
                    "numSensors": len(self.sensors)
                }
            }

            with open(filePath, 'w') as f:
                json.dump(modelData, f, indent=2)
            
            self.currentFilePath = filePath
            return True
        except Exception as e:
            print(f"Error saving model: {e}")
            return False

    def loadModel(self, filePath):
        """Load a model from JSON file"""
        try:
            with open(filePath, 'r') as f:
                data = json.load(f)
            
            # Clear current model
            self.clearAll()
            
            # Load points
            self.points = [Point(*coords) for coords in data.get("points", [])]
            
            # Load lines
            for idx1, idx2 in data.get("lines", []):
                if idx1 < len(self.points) and idx2 < len(self.points):
                    self.lines.append(Line(self.points[idx1], self.points[idx2]))
            
            # Load surfaces
            for pointIndices in data.get("surfaces", []):
                surfacePoints = [self.points[i] for i in pointIndices if i < len(self.points)]
                if len(surfacePoints) >= 3:
                    self.surfaces.append(Surface(surfacePoints))
            
            # Load sensors
            self.sensors = [Sensor(*coords) for coords in data.get("sensors", [])]
            
            self.currentFilePath = filePath
            self.updatePlot()
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False

    # ==================== Export Methods ==================== #

    def exportGltf(self, filePath):
        """Export the model to GLTF format"""
        try:
            scene = trimesh.Scene()
            
            # Export points as spheres
            for point in self.points:
                sphere = trimesh.creation.icosphere(radius=0.05)
                sphere.apply_translation(point.toNumpy())
                sphere.visual.face_colors = [255, 0, 0, 255]  # Red
                scene.add_geometry(sphere)
            
            # Export lines as cylinders
            for line in self.lines:
                cylinder = trimesh.creation.cylinder(
                    radius=0.02, 
                    height=line.length()
                )
                direction = line.directionVector()
                rotation = trimesh.geometry.align_vectors([0, 0, 1], direction)
                cylinder.apply_transform(rotation)
                cylinder.apply_translation(
                    (line.point1.toNumpy() + line.point2.toNumpy()) / 2
                )
                cylinder.visual.face_colors = [0, 255, 0, 255]  # Green
                scene.add_geometry(cylinder)
            
            # Export surfaces
            for surface in self.surfaces:
                if surface.getMesh():
                    vertices = surface.getMesh().points
                    faces = surface.getMesh().faces.reshape(-1, 4)[:, 1:4]
                    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
                    mesh.visual.face_colors = [0, 255, 0, 128]  # Semi-transparent green
                    scene.add_geometry(mesh)
            
            scene.export(filePath)
            return True
        except Exception as e:
            print(f"Error exporting GLTF: {e}")
            return False

    # ==================== Animation Methods ==================== #

    def animateSurface(self):
        """Animate the selected surface with a wave effect"""
        # Uncomment when surface selection is implemented
        # if not self.surfaces or not self.selectedSurfaces:
        #     return
        
        # surface = self.surfaces[self.selectedSurfaces[0]]
        # Again swicth when Surface Selection Implemented
        surface = self.surfaces[0]
        if not surface.getMesh():
            return
        
        # Apply wave deformation
        points = surface.getMesh().points.copy()
        amp = self.vib_amplitude# Amplitude
        freq = self.vib_frequency  # Frequency
        
        # Create wave pattern based on x,y position and phase
        points[:, 2] += amp * np.sin(
            freq * self.vibrationPhase + 
            points[:, 0] * self.vib_x_inf + 
            points[:, 1] * self.vib_y_inf
        )
        
        surface.getMesh().points = points
        self.vibrationPhase += 0.05
        self.plotter.update()

    def startVibration(self):
        """Start surface vibration animation"""
        if not self.vibrationTimer.isActive():
            surface = self.surfaces[0]  # Replace with selected surface if needed
            if surface.getMesh() and not hasattr(surface, "originalPoints"):
                surface.originalPoints = surface.getMesh().points.copy()

            self.vibrationTimer.start(self.vib_speed)  # ~20fps
            return True
        return False

    def stopVibration(self, restore_original=False):
        """Stop surface vibration animation
        Args:
            restore_original (bool): If True, reset to original surface.
                                     If False, keep current deformed shape.
        """
        if self.vibrationTimer.isActive():
            self.vibrationTimer.stop()

            surface = self.surfaces[0]  # Replace with selected surface if needed

            if restore_original and hasattr(surface, "originalPoints") and surface.getMesh():
                surface.getMesh().points = surface.originalPoints.copy()
                self.plotter.update()

            return True
        return False



    # ==================== Utility Methods ==================== #

    def clearAll(self):
        """Clear the entire model"""
        self.points.clear()
        self.lines.clear()
        self.surfaces.clear()
        self.sensors.clear()
        self.clearSelection()
        self.plotter.clear()
        self.plotter.reset_camera()

    def drawPointsAlongLine(self, numPoints: int):
        """Create points along a line between selected points"""
        if len(self.selectedPoints) < 2:
            return False
        
        # Get the line between first two selected points
        p1 = self.points[self.selectedPoints[0]]
        p2 = self.points[self.selectedPoints[1]]
        direction = p2.toNumpy() - p1.toNumpy()
        length = np.linalg.norm(direction)
        direction = direction / length  # Normalize
        
        # Create evenly spaced points along the line
        for i in range(1, numPoints + 1):
            fraction = i / (numPoints + 1)
            newPoint = p1.toNumpy() + direction * (length * fraction)
            self.points.append(Point(*newPoint))
        
        self.updatePlot()
        return True

    def checkCollinear(self, pointIndices):
        """Check if selected points are collinear"""
        if len(pointIndices) < 3:
            return True
        
        points = [self.points[i].toNumpy() for i in pointIndices]
        vec1 = points[1] - points[0]
        vec2 = points[2] - points[0]
        cross = np.cross(vec1, vec2)
        
        # Check if all subsequent points lie on the same line
        for i in range(3, len(points)):
            vec = points[i] - points[0]
            if not np.allclose(np.cross(vec, vec1), [0, 0, 0], atol=1e-6):
                return False
        
        return True
    

    #3D View Functions
    def showXYView(self):
        self.plotter.view_xy()
        self.plotter.reset_camera()

    def showYZView(self):
        self.plotter.view_yz()
        self.plotter.reset_camera()

    def showZXView(self):
        self.plotter.view_zx()
        self.plotter.reset_camera()

    def showIsometric(self):
        self.plotter.view_isometric()
        self.plotter.reset_camera()


    def rotateAroundPoint(self,point, position, up, angle_degrees):
        """Rotate position around point along 'up' vector by angle."""
        # Vector from point to camera
        vec = np.array(position) - np.array(point)
        angle_radians = np.radians(angle_degrees)

        # Normalize the up vector
        up = np.array(up)
        up = up / np.linalg.norm(up)

        # Rodrigues' rotation formula
        cos_a = np.cos(angle_radians)
        sin_a = np.sin(angle_radians)
        cross = np.cross(up, vec)
        dot = np.dot(up, vec)
        rotated = (vec * cos_a +
                   cross * sin_a +
                   up * dot * (1 - cos_a))

        return point + rotated

    def turn90Left(self):
        cam = self.plotter.camera
        pos = np.array(cam.GetPosition())
        focal = np.array(cam.GetFocalPoint())
        up = np.array(cam.GetViewUp())

        new_pos = self.rotateAroundPoint(focal, pos, up, 90)
        cam.SetPosition(*new_pos)
        cam.SetViewUp(*up)  # Keep same up direction
        self.plotter.render()

    def turn90Right(self):
        cam = self.plotter.camera
        pos = np.array(cam.GetPosition())
        focal = np.array(cam.GetFocalPoint())
        up = np.array(cam.GetViewUp())

        new_pos = self.rotateAroundPoint(focal, pos, up, -90)
        cam.SetPosition(*new_pos)
        cam.SetViewUp(*up)
        self.plotter.render()

    def fitToView(self):
        self.plotter.reset_camera()

    def takeSnapshot(self, filename="snapshot.png"):
        self.plotter.screenshot(filename)





    #========================= UTILARY DRAWING METHODS =========================#
    def drawRectangle(self,origin, origin_type, width, height, plane):
        x, y, z = origin

        # Default axis vectors based on the plane
        if plane == 'xy':
            axis_u = (1, 0, 0)  # width in x
            axis_v = (0, 1, 0)  # height in y
        elif plane == 'yz':
            axis_u = (0, 1, 0)  # width in y
            axis_v = (0, 0, 1)  # height in z
        elif plane == 'zx':
            axis_u = (0, 0, 1)  # width in z
            axis_v = (1, 0, 0)  # height in x
        else:
            raise ValueError("Invalid plane. Must be 'xy', 'yz', or 'zx'.")

        # Offset the origin if it's the center
        if origin_type == 'center':
            dx = -width / 2
            dy = -height / 2
        elif origin_type == 'corner':
            dx = 0
            dy = 0
        else:
            raise ValueError("origin_type must be 'center' or 'corner'.")

        # Helper to scale and shift a point
        def add_scaled(base, u_scale, u_vec, v_scale, v_vec):
            return (
                base[0] + u_scale * u_vec[0] + v_scale * v_vec[0],
                base[1] + u_scale * u_vec[1] + v_scale * v_vec[1],
                base[2] + u_scale * u_vec[2] + v_scale * v_vec[2],
            )

        # Compute corner points
        base_point = add_scaled(origin, dx, axis_u, dy, axis_v)
        corners = [
            base_point,
            add_scaled(base_point, width, axis_u, 0, axis_v),
            add_scaled(base_point, width, axis_u, height, axis_v),
            add_scaled(base_point, 0, axis_u, height, axis_v),
        ]

        self.points.append(Point(corners[0][0],corners[0][1],corners[0][2]))
        self.points.append(Point(corners[1][0],corners[1][1],corners[1][2]))
        self.points.append(Point(corners[2][0],corners[2][1],corners[2][2]))
        self.points.append(Point(corners[3][0],corners[3][1],corners[3][2]))

        self.updatePlot()


