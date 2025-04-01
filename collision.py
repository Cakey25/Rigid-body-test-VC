
import pygame as pg

def bounding_box(shape_a, shape_b):
    bound_a = shape_a.bounding_box
    bound_b = shape_b.bounding_box

    return (
        bound_a.left < bound_b.right and
        bound_a.right > bound_b.left and
        bound_a.bottom < bound_b.top and
        bound_a.top > bound_b.bottom
    )

def seperating_axis(shape_a, shape_b):
        edges = vertices_to_vectors(shape_a.vertices) + vertices_to_vectors(shape_b.vertices)
        axes = [pg.Vector2(edge.y, -edge.x).normalize() for edge in edges]

        for axis in axes:
            projection_a = project_vertices(shape_a.vertices, axis)
            projection_b = project_vertices(shape_b.vertices, axis)

            overlapping = overlap(projection_a, projection_b)
            if not overlapping:
                return False
        
        return True

def vertices_to_vectors(vertices):
    return [vertices[(i + 1) % len(vertices)] - vertices[i] for i in range(len(vertices))]

def project_vertices(vertices, axis):
    dots = [axis.dot(vertex) for vertex in vertices]
    return [min(dots), max(dots)]

def overlap(projection1, projection2):
    return min(projection1) <= max(projection2) and min(projection2) <= max(projection1)

def polygon_polygon(shape_a, shape_b):
    edges_a = vertices_to_lines(shape_a.vertices)
    edges_b = vertices_to_lines(shape_b.vertices)

    collisions = []
    for e_a in edges_a:
        for e_b in edges_b:
            if intersection := line_line(e_a, e_b):
                collisions += intersection

    return collisions

def line_line(line_a, line_b):
    # If both lines have a gradient of 0
    if line_a[1].x - line_a[0].x == 0 and line_b[1].x - line_b[0].x == 0:
        return False
    # If both lines are parallel
    if line_a[1].x - line_a[0].x != 0 and line_b[1].x - line_b[0].x != 0:
        grad_a = (line_a[1].y - line_a[0].y) / (line_a[1].x - line_a[0].x)
        grad_b = (line_b[1].y - line_b[0].y) / (line_b[1].x - line_b[0].x)
        if grad_a == grad_b:
            return False
    intersect_a = (
        ((line_b[1].x - line_b[0].x) * (line_a[0].y - line_b[0].y) -
        (line_b[1].y - line_b[0].y) * (line_a[0].x - line_b[0].x)) /
        ((line_b[1].y - line_b[0].y) * (line_a[1].x - line_a[0].x) -
        (line_b[1].x - line_b[0].x) * (line_a[1].y - line_a[0].y))
    )
    intersect_b = (
        ((line_a[1].x - line_a[0].x) * (line_a[0].y - line_b[0].y) -
        (line_a[1].y - line_a[0].y) * (line_a[0].x - line_b[0].x)) /
        ((line_b[1].y - line_b[0].y) * (line_a[1].x - line_a[0].x) -
        (line_b[1].x - line_b[0].x) * (line_a[1].y - line_a[0].y))
    )
    if 0 <= intersect_a <= 1 and 0 <= intersect_b <= 1:
        return [line_a, line_b]

    return False

def vertices_to_lines(vertices):
    return [(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]

def calculate_intersection(line_a, line_b, intersect_a, intersect_b):
        intersection = pg.Vector2(
            line_a[0].x + (intersect_a * (line_a[1].x - line_a[0].x)),
            line_b[0].y + (intersect_a * (line_a[1].y - line_a[0].y))
        )
        return intersection

def find_collision_points(edges):
    paired_edges = [(edges[e1], edges[e2]) for e1 in range(len(edges)) for e2 in range(e1+1,len(edges))]
    collisions = []
    for pair in paired_edges:
        if pair[0] == pair[1]:
            continue
        if point := edges_duplicate_vertices(*pair):
            if point not in collisions: 
                collisions.append(point)
            # Find normals
        
    return collisions
 
def edges_duplicate_vertices(line_a, line_b):
    points = [line_a[0], line_a[1], line_b[0], line_b[1]]
    temp = []
    for point in points:
        if point in temp: return point
        else: temp.append(point)
    return False

def find_normals(edges, points):
    # Very horriable way of finding normals
    if len(points) == 2:
        normal = (points[1] - points[0]).normalize().rotate(90)
        return normal

    for edge in edges:
        count = 0
        for comparison in edges:
            if edge == comparison:
                count += 1
        if count == 2:
            # Convension that point orders will always go anticlockwise
            point_1 = edge[0]
            point_2 = edge[1]
            tangent = point_2 - point_1
            # Calculate the normal to the edge
            normal = pg.Vector2(tangent.y, -tangent.x).normalize()
            return normal
        
def calc_midpoint(p1, p2):
    return (p1 + p2) / 2








