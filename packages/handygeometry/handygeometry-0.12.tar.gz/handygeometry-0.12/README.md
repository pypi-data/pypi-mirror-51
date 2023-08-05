<img src="G01.jpg" height="60px">

# geometry
A collection of handy geometry functions.
Area, Volumes, Perimeters, Surface Area, Inscribed and circumscribed calculations and much more.. 

## Area
- square(a)
- rectangle(length, width)
- triangle(base, height)
  - triangle_three_sides(a, b, c)
  - triangle_two_sides_and_angle_SAS(a, b, angle)
  - triangle_two_angles_and_side_ASA
- circle(r)
  - circle_sector(r, angle)
- ellipse(a, b)
- trapezoid(a, b, height)
- parallelogram(base, height)
  - paralelogram_two_sides_and_angle(a, b, angle)
  - paralelogram_diagonals_and_an_angle(e, f, angle)
- rhombus(side, height)
  - rhombus_diagonals(e, f)
  - rhombus_side_and_any_angle(side, angle)
- kite_diagonals(e, f)
  - kite_two_unequal_sides_and_angle(a, b, angle)
- regular_pentagon(a)
- regular_hexagon(a)
- regular_octagon(a)
- annulus(R, r)
- irregualar_quadrilateral(e, f, angle)
- regular_polygon(sides, a)


## Perimeters
- square(a)
- rectangle(a, b)
- triangle_three_sides_SSS(a, b, c)
    triangle_two_sides_and_angle_SAS(a, b, angle)
    triangle_two_angles_and_side_ASA(a, angle1, angle2)
- circle(r)
    circle_sector(r, angle)
- ellipse(a, b)
- quadrilateral(a, b, c, d)
- trapezoid(a, b, c, d)
- parallelogram_sides(a, b)
  - parallelogram_one_side_and_diagonals(a, e, f)
  - parallelogram_base_heigt_any_angle(base, height, angle)
- rhombus_side(a)
  - rhombus_diagonals(e, f)
- kite(a, b)
- annulus(R, r)
- regular_polygon(sides, a)



## Volumes
- cube(s)
- cylinder(r, height)
  - hollow_cylinder(R, r, height)
- pyramid(base_area, height)
  - pyramid_with_regular_base(shape_of_base, height, side_length)
- cone(r, height)
  - truncated_cone(lower_r, upper_r, height)
- ellipsoid(a, b, c)
- torus(a, b)
- rectangular_cuboid
- regular_tetrahedron(a)
- obelisk (a,b,A,B, height)
- wedge (a,b,c, height)
- frustum(s1, s2, height)


## Surface Area
- wedge(a, b, c, height)
- regular_tetrahedron(a)
- torus(a, b)
- sphere(r)
- cube(a)
- cylinder(r, height)
  - lateral_cylinder(r, height)
  - base_cylinder(r)
- cone(r, height)
  - lateral_cone(r, height)
  - base_cone(r, height)
- rectangular_prism_box(a, b, c)
- triangular_prism(a, b, c, height)
- pyramid(l, height)
  - base_pyramid(l)
  - lateral_pyramid(l, height)

## Inscribed and circumscribed
- incircle_of_a_triangle(a, b, c)
- incircle_of_a_regular_polygon(n, a)
- regular_polygons_inscribed_to_a_circle(n, r)
- circumcircle_of_a_triangle(a, b, c)
- circumcircle_of_a_regular_polygon(n, a)
- regular_polygon_circumscribed_to_a_circle(n, r)

## others
- edge_length_cube(V)
- angles_of_a_triangle(a,b,c)
- regular_polyhedrons(n,a)
    (volume, surface area,radii of inscribed and circumscribed spheres calculations)
    -tetrahedron(4), cube(6), octahedron(8), dodecahedron(12), icosahedron(20)
- vector_norm(*args)
