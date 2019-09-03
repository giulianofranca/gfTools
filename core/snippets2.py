# 1- Get the aim vector | v2 - v1
# 2- Get the length of aim Vector | vAim.length()
# 3- Compute cone attrs
# 4- Set the cone location to start point | vConeLocation = v1
# 5- Initialize a matrix | mat44 = om2.MMatrix()
# 6- Start vector is the aim vector normalized | vStart = vAim.normal()
# 7- Normalize the Z Axis to get end vector | vEnd = om2.MFloatVector(0.0, 0.0, 1.0)
# 8- If vectors are identical, set the matrix to ID | if vStart - vEnd > 1e-14: mat44 = om2.MMatrix()
#    Else create the matrix
#    8.1- Cross vStart with vEnd | axb = vStart ^ vEnd
#    8.2- Normalize the axb | nAxb = axb.normal()
#    8.3- Find angle between start and end vectors | ac = acos(dot(vStart, vEnd))
#    8.4- Calculate attribs | s = sin(ac); c = cos(ac); t = 1 - c
#    8.5- Calculate XYZ | x = nAxb.x; y = nAxb.y; z = nAxb.z
#    8.6- Fill the matrix
#        mat44[0] = t * x * x + c
#        mat44[1] = t * x * y - s * z
#        mat44[2] = t * x * z + s * y
#        mat44[4] = t * x * y + s * z
#        mat44[5] = t * y * y + c
#        mat44[6] = t * y * z - s * x
#        mat44[8] = t * x * z - s * y
#        mat44[9] = t * y * z + s * x
#        mat44[10] = t * z * z + c
#        mat44[15] = 1.0
# 9- Multiply cone location to the rotation matrix | vFinal = vConeLocation * mat44