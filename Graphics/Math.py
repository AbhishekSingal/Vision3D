import math
from scipy.spatial import ConvexHull
import numpy as np

def sectionFormula(p1, p2, f1, f2):
    """
    Calculate the coordinates of a point dividing the line segment between p1 and p2
    in the ratio f1:f2.

    Parameters:
        p1 (list or tuple): [x1, y1, z1] - first point
        p2 (list or tuple): [x2, y2, z2] - second point
        f1 (float or int): Ratio part for p1
        f2 (float or int): Ratio part for p2

    Returns:
        list: [x, y, z] coordinates of the section point
    """
    if f1 + f2 == 0:
        raise ValueError("The sum of f1 and f2 must not be zero (division by zero).")

    x = (f2 * p1[0] + f1 * p2[0]) / (f1 + f2)
    y = (f2 * p1[1] + f1 * p2[1]) / (f1 + f2)
    z = (f2 * p1[2] + f1 * p2[2]) / (f1 + f2)

    return [x, y, z]

def insertEquallySpacedPoints(p1, p2, n):
    """
    Insert `n` equally spaced points between two points p1 and p2.

    Parameters:
        p1 (list or tuple): [x1, y1] or [x1, y1, z1]
        p2 (list or tuple): [x2, y2] or [x2, y2, z2]
        n (int): Number of points to insert **between** p1 and p2

    Returns:
        list: A list of `n` equally spaced points (excluding p1 and p2)
    """
    if len(p1) != len(p2):
        raise ValueError("Points must have the same dimensions (2D or 3D).")

    points = []
    for i in range(1, n + 1):
        ratio = i / (n + 1)  # normalize between 0 and 1, excluding endpoints
        point = [(1 - ratio) * p1[j] + ratio * p2[j] for j in range(len(p1))]
        points.append(point)

    return points


def computePlaneNormal(p1, p2, p3):
    """
    Compute the normal vector of the plane defined by three points.
    """
    u = [p2[i] - p1[i] for i in range(3)]
    v = [p3[i] - p1[i] for i in range(3)]
    # Cross product
    normal = [
        u[1]*v[2] - u[2]*v[1],
        u[2]*v[0] - u[0]*v[2],
        u[0]*v[1] - u[1]*v[0]
    ]
    # Normalize the normal vector
    length = math.sqrt(sum(c**2 for c in normal))
    if length == 0:
        raise ValueError("Degenerate plane — points may be colinear.")
    return [c / length for c in normal]

def generateOffsetCopies(points, dist, reps):
    """
    Generate `reps` copies of a coplanar set of 3D points, offset along the plane's normal.

    Parameters:
        points (list of [x, y, z]): Coplanar 3D points
        dist (float): Distance to offset each layer
        reps (int): Number of layers to generate

    Returns:
        list of list of [x, y, z]: List of point sets, each offset by (normal * dist * i)
    """
    if len(points) < 3:
        raise ValueError("At least 3 points are required to define a plane.")

    normal = computePlaneNormal(points[0], points[1], points[2])
    allLayers = []

    for i in range(1, reps + 1):
        offset = [normal[j] * dist * i for j in range(3)]
        layer = [[p[0] + offset[0], p[1] + offset[1], p[2] + offset[2]] for p in points]
        allLayers.append(layer)

    return allLayers


def connectCoplanarPoints3D(points):
    """
    Connects 3D coplanar points in border order.
    
    Parameters:
        points (list of list/tuple): List of [x, y, z] 3D coordinates.
        
    Returns:
        list of tuple: List of (point1, point2) tuples, each point as a 3D tuple.
    """
    if len(points) < 3:
        raise ValueError("At least 3 points are required to form a border.")
    
    # Convert to numpy array
    pts = np.array(points)
    
    # Step 1: Find a best-fit plane for projection
    centroid = np.mean(pts, axis=0)
    centered_pts = pts - centroid
    
    # PCA to get the 2 main directions (plane basis vectors)
    u, s, vh = np.linalg.svd(centered_pts)
    plane_axes = vh[:2]  # First two principal components define the plane

    # Step 2: Project 3D points to 2D plane coordinates
    pts_2d = centered_pts @ plane_axes.T  # Project onto 2D plane

    # Step 3: Compute convex hull in 2D
    hull = ConvexHull(pts_2d)
    hull_indices = hull.vertices
    
    # Step 4: Return edges in order using original 3D points
    connections = []
    for i in range(len(hull_indices)):
        p1 = tuple(pts[hull_indices[i]])
        p2 = tuple(pts[hull_indices[(i + 1) % len(hull_indices)]])
        connections.append((p1, p2))
    
    return connections

def distance3D(p1, p2):
    """
    Calculates the Euclidean distance between two 3D points.

    Parameters:
        p1 (tuple or list): First point (x1, y1, z1)
        p2 (tuple or list): Second point (x2, y2, z2)

    Returns:
        float: The 3D distance between p1 and p2
    """
    return math.sqrt(
        (p1[0] - p2[0])**2 +
        (p1[1] - p2[1])**2 +
        (p1[2] - p2[2])**2
    )
