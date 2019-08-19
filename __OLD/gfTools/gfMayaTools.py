import sys
import maya.cmds as cmds
from functools import partial


class gfMayaTools(object):

    def __init__(self):
        mayaVersion = cmds.about(version=True)
        supportedVersions = ['2017', '2018']
        if mayaVersion not in supportedVersions:
            sys.stderr.write('[ Application Error ]\tgfMayaTools not supported in this Maya version | Supported versions: %s' %(', '.join(supportedVersions)))
            sys.exit()
        self.gui()

    def verifyUI(self):
        if(cmds.window(self.widgets['WindowName'], exists=True)):
            cmds.deleteUI(self.widgets['WindowName'])
        if(cmds.workspaceControl(self.widgets['WorkspaceName'], exists=True)):
            cmds.deleteUI(self.widgets['WorkspaceName'])

    def closeWindow(self, *args):
        cmds.deleteUI(self.widgets['WindowName'])
        cmds.deleteUI(self.widgets['WorkspaceName'])

    def gui(self):
        self.widgets = {}
        self.widgets['WindowName'] = "wingfMayaToolsWin"
        self.widgets['WorkspaceName'] = "wingfMayaToolsDock"
        self.widgets['CloseUI'] = "btnCloseUI"
        self.widgets['ShelfTabs'] = "slfMainShelfTab"
        self.bgColor = [0.164706, 0.164706, 0.164706]
        self.verifyUI()

        cmds.window(self.widgets['WindowName'], wh=[275, 600], t="gfMayaTools", mxb=False, mb=True, mbv=True, tb=False)
        cmds.menu(l="Help", helpMenu=True)
        cmds.menuItem(l="How to Use")
        cmds.menuItem(d=True)
        cmds.menuItem(l="About Application")
        mainControl = cmds.workspaceControl(self.widgets['WorkspaceName'], iw=275, mw=True, l='gfMayaTools',
            dtc=['ToolBox', 'right'], wp='preferred', fl=True)
        cmds.workspaceControl(self.widgets['WorkspaceName'], e=True, vis=True)
        cmds.workspaceControl(self.widgets['WorkspaceName'], e=True, r=True)
        cmds.evalDeferred(lambda *args: cmds.workspaceControl(mainControl, e=True, r=True))
        cmds.button(self.widgets['CloseUI'], l="Close Window", h=5, c=partial(self.closeWindow))
        cmds.shelfTabLayout(self.widgets['ShelfTabs'], i="smallTrash.png", iv=True, snt=True, tc=False, ntc='cmds.warning("In Development")')
        cmds.shelfLayout("Default")
        # --------------------------------------------------------------------------------------------------
        # FILES
        # --------------------------------------------------------------------------------------------------
        # New Scene
        self.setShelfButton("Create a new scene", "NewScene", "NS", "menuIconFile.png", "NewScene", "mel", "")

        # Save Scene As
        self.setShelfButton("Save the current scene under a new name or export all", "Save Scene As...", "SSA", "menuIconFile.png", "SaveSceneAs", "mel", "")

        # Project Window
        self.setShelfButton("Create a new project or edit the current project", "Project Window", "PW", "menuIconFile.png", "ProjectWindow", "mel", "")

        # Set Project
        self.setShelfButton("Change the current project", "Set Project...", "SP", "menuIconFile.png", "SetProject", "mel", "")

        # Open Scene
        self.setShelfButton("Open a scene", "Open Scene...", "OS", "menuIconFile.png", "OpenScene", "mel", "")

        # Import
        self.setShelfButton("Add the file to the current scene", "Import...", "Impo", "menuIconFile.png", "Import", "mel", "")

        # Export Selection
        self.setShelfButton("Export selected objects (and related info) to a new file", "Export Selection...", "ES", "menuIconFile.png", "ExportSelection", "mel", "")

        # Reference Editor
        self.setShelfButton("Edit the references for the current scene", "Reference Editor", "RE", "menuIconFile.png", "ReferenceEditor", "mel", "")

        # --------------------------------------------------------------------------------------------------
        # EDITORS
        # --------------------------------------------------------------------------------------------------
        # Outliner
        self.setShelfButton("List the objects in the scene", "Outliner", "Outl", "menuIconWindow.png", "OutlinerWindow", "mel", "")

        # Graph Editor
        self.setShelfButton("Edit animation curves", "Graph Editor", "GE", "menuIconWindow.png", "GraphEditor", "mel", "")

        # Conection Editor
        self.setShelfButton("Make connections between object attributes", "Connection Editor", "CE", "menuIconWindow.png", "ConnectionEditor", "mel", "")

        # Expression Editor
        self.setShelfButton("Edit expressions between attributes", "Expression Editor", "EE", "menuIconWindow.png", "ExpressionEditor", "mel", "")

        # Node Editor
        self.setShelfButton("Display relationships among nodes in your scene graphically", "Node Editor", "NE", "menuIconWindow.png", "NodeEditorWindow", "mel", "")

        # Component Editor
        self.setShelfButton("Edit various component values for the selected object(s)", "Component Editor", "CpEd", "menuIconWindow.png", "ComponentEditor", "mel", "")

        # Attribute Spread Sheet
        self.setShelfButton("Edit the attributes of the selected object(s)", "Attribute Spread Sheet", "SpSh", "menuIconWindow.png", "SpreadSheetEditor", "mel", "")

        # Sets
        self.setShelfButton("Edit set membership", "Sets", "Sets", "menuIconWindow.png", "SetEditor", "mel", "")

        # Camera Sequencer
        self.setShelfButton("Non-linear camera sequence editor", "Camera Sequencer", "CS", "menuIconWindow.png", "SequenceEditor", "mel", "")

        # Dope Sheet
        self.setShelfButton("Perform high-level timing and animation event and sound synchronization editing", "Dope Sheet", "DS", "menuIconWindow.png", "DopeSheetEditor", "mel", "")

        # Namespace Editor
        self.setShelfButton("Namespace Editor", "Namespace Editor", "NE", "menuIconWindow.png", "NamespaceEditor", "mel", "")

        # Edit Layouts
        self.setShelfButton("Edit the panel layouts", "Panel Editor", "PE", "menuIconWindow.png", "PanelPreferencesWindow", "mel", "")

        # --------------------------------------------------------------------------------------------------
        # MODIFY
        # --------------------------------------------------------------------------------------------------
        # Local Rotation Axis
        self.setShelfButton("Toggle local rotation axis visibility", "Local Rotation Axes", "LRA", "menuIconDisplay.png", "ToggleLocalRotationAxes", "mel", "")

        # Toggle Normals
        self.setShelfButton("Toggle visible normals in shaded mode", "Normals (Shaded Mode)", "Nrm", "menuIconDisplay.png", "ToggleNormals", "mel", "")

        # Toggle Cv
        self.setShelfButton("Toggle CV visibility", "CVs", "CVs", "menuIconDisplay.png", "ToggleCVs", "mel", "")

        # Toggle Vertices
        self.setShelfButton("Toggle poly vertex visibility", "Vertices", "Vert", "menuIconDisplay.png", "ToggleVertices", "mel", "")

        # Toggle Scale Pivot
        self.setShelfButton("Toggle scale pivot visibility", "Scale Pivots", "SP", "menuIconDisplay.png", "ToggleScalePivots", "mel", "")

        # Select Hierarchy
        self.setShelfButton("Select all the children of the current selection", "Hierarchy", "Hier", "menuIconSelect.png", "SelectHierarchy", "mel", "")

        # Bezier to NURBS
        self.setShelfButton("Select Bezier curve(s)", "Bezier Curve to NURBS", "BCtN", "menuIconModify.png", "bezierCurveToNurbs", "mel", "")

        # Search and Replace Names
        self.setShelfButton("Rename objects in scene", "Search and Replace Names...", "SaRN", "menuIconModify.png", "performSearchReplaceNames 1", "mel", "")

        # Freeze Transformations
        self.setShelfButton("Select an object(s)", "Freeze Transformations", "FT", "menuIconModify.png", "FreezeTransformations", "mel", "")

        # Center Pivot
        self.setShelfButton("Select an object(s)", "Center Pivot", "CP", "menuIconModify.png", "CenterPivot", "mel", "")

        # Delete History
        self.setShelfButton("Delete construction history on the selected object(s)", "History", "Hist", "menuIconEdit.png", "DeleteHistory", "mel", "")

        # Quick Selection Set
        self.setShelfButton("Create set and add it to the Quick Select Set Menu", "Quick Select Set...", "QSS", "menuIconEdit.png", "CreateQuickSelectSet", "mel", "")

        # Set Driven Key
        self.setShelfButton("Set driven key options", "Set...", "Set.", "menuIconKeys.png", "SetDrivenKeyOptions", "mel", "")

        # Set Annotation
        self.setShelfButton("Add an annotation to the selected object", "Annotation...", "", "annotation.png", "CreateAnnotateNode", "mel", "")

        # Create Camera
        self.setShelfButton("Create a camera on the grid", "Camera", "", "view.png", "camera -centerOfInterest 5 -focalLength 35 -lensSqueezeRatio 1 -cameraScale 1 -horizontalFilmAperture 1.41732 -horizontalFilmOffset 0 -verticalFilmAperture 0.94488 -verticalFilmOffset 0 -filmFit Fill -overscan 1 -motionBlur 0 -shutterAngle 144 -nearClipPlane 0.1 -farClipPlane 10000 -orthographic 0 -orthographicWidth 30 -panZoomEnabled 0 -horizontalPan 0 -verticalPan 0 -zoom 1; objectMoveCommand;", "mel", "CreateCameraOnlyOptions")

        # --------------------------------------------------------------------------------------------------
        # MODELING
        # --------------------------------------------------------------------------------------------------
        # Create Plane
        self.setShelfButton("Create a polygonal plane on the grid", "Plane", "", "polyMesh.png", "polyPlane -w 1 -h 1 -sx 10 -sy 10 -ax 0 1 0 -cuv 2 -ch 1; objectMoveCommand;", "mel", "CreatePolygonPlaneOptions")

        # Create Sphere
        self.setShelfButton("Create a polygonal sphere on the grid", "Sphere", "", "polySphere.png", "polySphere -r 1 -sx 20 -sy 20 -ax 0 1 0 -cuv 2 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreatePolygonSphereOptions")

        # Create Cube
        self.setShelfButton("Create a polygonal cube on the grid", "Cube", "", "polyCube.png", "polyCube -w 1 -h 1 -d 1 -sx 1 -sy 1 -sz 1 -ax 0 1 0 -cuv 4 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreatePolygonCubeOptions")

        # Create Cylinder
        self.setShelfButton("Create a polygonal cylinder on the grid", "Cylinder", "", "polyCylinder.png", "polyCylinder -r 1 -h 2 -sx 20 -sy 1 -sz 1 -ax 0 1 0 -rcp 0 -cuv 3 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreatePolygonCylinderOptions")

        # Create Torus
        self.setShelfButton("Create a polygonal torus on the grid", "Torus", "", "polyTorus.png", "polyTorus -r 1 -sr 0.5 -tw 0 -sx 20 -sy 20 -ax 0 1 0 -cuv 1 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreatePolygonTorusOptions")

        # Extract Faces
        self.setShelfButton("Extract the currently selected faces from their shell and show a manipulator to adjust their offset", "Extract", "", "polyChipOff.png", "performPolyChipOff 0 0", "mel", "ExtractFaceOptions")

        # Multi-Cut
        self.setShelfButton("Tools to cut, slice, and insert edges on polygons", "Multi-Cut", "", "multiCut_NEX32.png", "dR_multiCutTool", "mel", "dR_multiCutTool; toolPropertyWindow;")

        # Reverse Normals
        self.setShelfButton("Reverse the normals of the selected faces", "Reverse", "", "polyNormal.png", "ReversePolygonNormals", "mel", "ReversePolygonNormalsOptions")

        # Set to Face
        self.setShelfButton("Set the normals of selected vertices or vertex-faces to their face normals and unshare them", "Set to Face", "", "polyNormalSetToFace.png", "polySetToFaceNormal", "mel", "SetToFaceNormalsOptions")

        # Combine
        self.setShelfButton("Combine the selected polygon objects into one single object to allow operations such as merges or face trims", "Combine", "", "polyUnite.png", "polyPerformAction polyUnite o 0", "mel", "")

        # Separate
        self.setShelfButton("Separate the selected polygon object shells or the shellfs of any selected faces from the object into distinct objects", "Separate", "", "polySeparate.png", "SeparatePolygon", "mel", "")

        # Grab Tool
        self.setShelfButton("Grab Tool: Pull a single vertex along a surface in any direction", "Grab Tool", "", "Grab.png", "SetMeshGrabTool", "mel", "ShowMeshGrabToolOptions")

        # Sculpt Tool
        self.setShelfButton("Sculpt Tool: Lift a surface", "Sculpt Tool", "", "Sculpt.png", "SetMeshSculptTool", "mel", "ShowMeshSculptToolOptions")

        # Wax Tool
        self.setShelfButton("Wax Tool: Build up a surface", "Wax Tool", "", "Wax.png", "SetMeshWaxTool", "mel", "ShowMeshWaxToolOptions")

        # Pinch Tool
        self.setShelfButton("Pinch Tool: Sharpen soft edges", "Pinch Tool", "", "Pinch.png", "SetMeshPinchTool", "mel", "ShowMeshPinchToolOptions")

        # Flatten Tool
        self.setShelfButton("Flatten Tool: Level a surface", "Flatten Tool", "", "Flatten.png", "SetMeshFlattenTool", "mel", "ShowMeshFlattenToolOptions")

        # Knife Tool
        self.setShelfButton("Knife Tool: Cut fine strokes into a surface", "Knife Tool", "", "Knife.png", "SetMeshKnifeTool", "mel", "ShowMeshKnifeToolOptions")

        # Bulge Tool
        self.setShelfButton("Bulge Tool: Inflate an area on a surface", "Bulge Tool", "", "Bulge.png", "SetMeshBulgeTool", "mel", "ShowMeshBulgeToolOptions")

        # Freeze Tool
        self.setShelfButton("Freeze Tool: Paint areas of a surface to prevent further modification", "Freeze Tool", "", "Freeze.png", "SetMeshFreezeTool", "mel", "ShowMeshFreezeToolOptions")

        # Sculpt Geometry Tool
        self.setShelfButton("Sculpt a geometry object", "Sculpt Geometry Tool", "", "putty.png", "SculptGeometryTool", "mel", "SculptGeometryToolOptions")

        # --------------------------------------------------------------------------------------------------
        # NURBS
        # --------------------------------------------------------------------------------------------------
        # NURBS Plane
        self.setShelfButton("Create a NURBS plane on the grid", "Plane", "", "plane.png", "nurbsPlane -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -d 3 -u 1 -v 1 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSPlaneOptions")

        # NURBS Circle
        self.setShelfButton("Create a NURBS circle on the grid", "Circle", "", "circle.png", "circle -c 0 0 0 -nr 0 1 0 -sw 360 -r 10 -d 3 -ut 0 -tol 0.01 -s 8 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSCircleOptions")

        # NURBS Sphere
        self.setShelfButton("Create a NURBS sphere on the grid", "Sphere", "", "sphere.png", "sphere -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -r 1 -d 3 -ut 0 -tol 0.01 -s 8 -nsp 4 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSSphereOptions")

        # NURBS Cube
        self.setShelfButton("Create a NURBS cube on the grid", "Cube", "", "cube.png", "nurbsCube -p 0 0 0 -ax 0 1 0 -w 1 -lr 1 -hr 1 -d 3 -u 1 -v 1 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSCubeOptions")

        # NURBS Cylinder
        self.setShelfButton("Create a NURBS cylinder on the grid", "Cylinder", "", "cylinder.png", "cylinder -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -r 1 -hr 2 -d 3 -ut 0 -tol 0.01 -s 8 -nsp 1 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSCylinderOptions")

        # NURBS Torus
        self.setShelfButton("Create a NURBS torus on the grid", "Torus", "", "torus.png", "torus -p 0 0 0 -ax 0 1 0 -ssw 0 -esw 360 -msw 360 -r 1 -hr 0.5 -d 3 -ut 0 -tol 0.01 -s 8 -nsp 4 -ch 1; objectMoveCommand; scale -r 50 50 50;", "mel", "CreateNURBSTorusOptions")

        # Extrude Surface
        self.setShelfButton("Select curve(s), isoparm(s) or trim edge(s); select path last", "Extrude", "", "extrude.png", "performSweepPreset(1,1,1,2,0,0,1,1,0,0,1,0,1,3)", "mel", "ExtrudeOptions")

        # CV Curve Tool
        self.setShelfButton("Create a curve on the grid or live surface specifying control vertices", "CV Curve Tool", "", "curveCV.png", "CVCurveTool", "mel", "CVCurveToolOptions")

        # EP Curve Tool
        self.setShelfButton("Create a curve on the grid or live surface spacifying edit points", "EP Curve Tool", "", "curveEP.png", "EPCurveTool", "mel", "EPCurveToolOptions")

        # Bezier Curve Tool
        self.setShelfButton("Bezier curve tool", "Bezier Curve Tool", "", "curveBezier.png", "CreateBezierCurveTool", "mel", "CreateBezierCurveToolOptions")

        # Rebuild Curve
        self.setShelfButton("Rebuild curve options", "Rebuild Curve Option Box", "", "rebuildCurve.png", "RebuildCurveOptions", "mel", "")

        # Edit Curve Tool
        self.setShelfButton("Select a curve or curve on surface", "Edit Curve Tool", "", "curveEditor.png", "CurveEditTool", "mel", "")

        # CV Hardness
        self.setShelfButton("Select control vertices on curve", "CV Hardness", "", "cvHardness.png", "performHardenPointCurvePreset 1 1 -1", "mel", "")

        # Reverse Curve Direction
        self.setShelfButton("Select curve(s)", "Reverse Direction", "", "reverse.png", "reversePreset 1 1 0", "mel", "")

        # Loft
        self.setShelfButton("Select curve(s), isoparm (s) or trim edge(s)", "Loft", "", "skin.png", r"doPerformLoft(\"1\", {\"1\",\"1\",\"1\",\"0\",\"3\",\"1\",\"0\",\"0\"} )", "mel", "")

        # Insert Isoparms
        self.setShelfButton("Select isoparm(s)", "Insert Isoparms", "", "insert.png", "insertKnowPreset 1 1 1 1 0 0", "mel", "")

        # Rebuild Surface
        self.setShelfButton("Rebuild surfaces options", "rebuildSurfaceDialogItem", "", "rebuildSurface.png", "RebuildSurfacesOptions", "mel", "")

        # Reverse Surface Direction
        self.setShelfButton("Select surface(s) or isoparm(s) to give direction", "Reverse Direction", "", "reverseSurface.png", "reversePreset 1 1 0", "mel", "")

        # Create Hair Options
        self.setShelfButton("Create hair options", "menuItem5532", "Cho", "menuIconHair.png", "CreateHairOptions", "mel", "")

        # Distance Tool
        self.setShelfButton("Measure distance between two points", "Distance Tool", "", "distanceDim.png", "DistanceTool", "mel", "")

        # Parameter Tool
        self.setShelfButton("Display a curve/surface point's parameter values", "Parameter Tool", "", "paramDim.png", "ParameterTool", "mel", "")

        # Arc Length Tool
        self.setShelfButton("Display a curve point's distance from the start of the curve", "Arc Length Tool", "", "arcLengthDim.png", "ArcLengthTool", "mel", "")

        # Attach to Motion Path
        self.setShelfButton("Select object(s) to animate along a motion path, followed by the motion path curve", "Attach to Motion Path", "", "motionPath.png", r"pathAnimation -fractionMode true -follow true -followAxis x -upAxis y -worldUpType \"vector\" -worldUpVector 0 1 0 -inverseUp false -inverseFront false -bank false -startTimeU `playbackOptions -query -minTime` -endTimeU  `playbackOptions -query -maxTime`", "mel", "")

        # Flow Path Object
        self.setShelfButton("Select path animated object(s) to flow along a motion path", "Flow Path Object", "", "flowPathObj.png", "flowObjects 200 2 2 1 0 2 2 2", "mel", "FlowPathObjectOptions")

        # --------------------------------------------------------------------------------------------------
        # SKELETON
        # --------------------------------------------------------------------------------------------------
        # Create Joints
        self.setShelfButton("Click to place joint. Click on existing joint to add to skeleton. Click-Drag to position joint.", "Create Joints", "", "kinJoint.png", "JointTool", "mel", "")

        # Orient Joints Options
        self.setShelfButton("Orient joint options", "orientJointOptionItem", "", "orientJoint.png", "OrientJointOptions", "mel", "")

        # Mirror Joints Options
        self.setShelfButton("Mirror joint options", "mirrorJointOptionItem", "", "kinMirrorJoint_S.png", "MirrorJointOptions", "mel", "")

        # IK Handle Tool Options
        self.setShelfButton("IK handle tool options", "handleDialogItem", "", "kinHandle.png", "IKHandleToolOptions", "mel", "")

        # IK Spline Handle Tool Options
        self.setShelfButton("IK spline handle tool options", "handleSplineDialogItem", "", "kinSplineHandle.png", "IKSplineHandleToolOptions", "mel", "")

        # Cluster
        self.setShelfButton("Select object(s)", "Cluster", "", "cluster.png", "CreateCluster", "mel", "")

        # Locator
        self.setShelfButton("Create a locator object on the grid", "Locator", "", "locator.png", "CreateLocator", "mel", "")

        # Blend Shape Options
        self.setShelfButton("Blend shape options", "blendShapeDialogItem", "", "blendShape.png", "CreateBlendShapeOptions", "mel", "")

        # Lattice
        self.setShelfButton("Select object(s)", "Lattice", "", "lattice.png", "CreateLattice", "mel", "")

        # Parent Constraint
        self.setShelfButton("Select one or more targets followed by the object to constrain.", "Parent", "", "parentConstraint.png", r"doCreateParentConstraintArgList 1 { \"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"\",\"1\" };", "mel", "ParentConstraintOptions")

        # Point Contraint
        self.setShelfButton("Select one or more targets followed by the object to constrain.", "Point", "", "posConstraint.png", r"doCreatePointConstraintArgList 1 { \"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"\",\"1\" };", "mel", "PointConstraintOptions")

        # Orient Constraint
        self.setShelfButton("Select one or more targets followed by the object to constrain.", "Orient", "", "orientConstraint.png", r"doCreateOrientConstraintArgList 1 { \"1\",\"0\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"\",\"1\" };", "mel", "OrientConstraintOptions")

        # Scale Constraint
        self.setShelfButton("Select one or more targets followed by the object to constrain.", "Scale", "", "scaleConstraint.png", r"doCreateScaleConstraintArgList 1 { \"1\",\"1\",\"1\",\"1\",\"0\",\"0\",\"0\",\"1\",\"\",\"1\" };", "mel", "ScaleConstraintOptions")

        # Aim Constraint
        self.setShelfButton("Select one or more targets followed by the object to constrain.", "Aim", "", "aimConstraint.png", r"doCreateAimConstraintArgList 1 { \"0\",\"0\",\"0\",\"0\",\"1\",\"0\",\"0\",\"0\",\"1\",\"0\",\"0\",\"1\",\"0\",\"1\",\"vector\",\"\",\"0\",\"0\",\"0\",\"\",\"1\" };", "mel", "AimConstraintOptions")

        # Pole Vector Constraint
        self.setShelfButton("Select one or more targets followed by the Rotate Plane ikHandle to constrain.", "Pole Vector", "", "poleVectorConstraint.png", "poleVectorConstraint -weight 1", "mel", "PoleVectorConstraintOptions")

        # --------------------------------------------------------------------------------------------------
        # SKIN
        # --------------------------------------------------------------------------------------------------
        # Skin Cluster
        self.setShelfButton("Select surface(s) and a joint.", "Bind Skin", "", "smoothSkin.png", "SmoothBindSkin", "mel", "SmoothBindSkinOptions")

        # Interactive Skin
        self.setShelfButton("Select surface(s) and a joint.", "Interactive Bind Skin", "", "interactiveBindTool.png", "InteractiveBindSkin", "mel", "InteractiveBindSkinOptions")

        # Unbind Skin
        self.setShelfButton("Select surface(s).", "Unbind Skin", "", "detachSkin.png", "DetachSkin", "mel", "DetachSkinOptions")

        # Add Influence
        self.setShelfButton("Select skinned surface(s) and influence transform(s).", "Add Influence", "", "addWrapInfluence.png", "AddInfluence", "mel", "AddInfluenceOptions")

        # Remove Influence
        self.setShelfButton("Select surface(s) first an then the influence transform", "Remove Influence", "", "removeWrapInfluence.png", "RemoveInfluence", "mel", "")

        # Remove Unused Influences
        self.setShelfButton("Select the skin and unused joints and influences will be disconnected to improve performance.", "Remove Unused Influence", "RUI", "menuIconSkinning.png", "removeUnusedInfluences", "mel", "")

        # Character Set
        self.setShelfButton("Attributes on the selected objects will be placed in a character set", "Create Character Set", "CCS", "menuIconKeys.png", r"doCreateCharacterArgList 4 { \"character1\",\"0\",\"0\",\"1\",\"1\",\"0\",\"0\",\"0\",\"0\",\"0\" };", "mel", "CreateCharacterOptions")

        # Subcharacter Set
        self.setShelfButton("Make highlighted Channel Box items a subcharacter of the current character", "Create Subcharacter Set", "CSS", "menuIconKeys.png", r"doCreateSubcharacterArgList 2 { \"subCharacter1\",\"0\",\"0\",\"1\",\"1\",\"0\",\"0\" };", "mel", "CreateSubCharacterOptions")

        # Add to Character Set
        self.setShelfButton("Add highlighted Channel Box items to current character set", "Add to Character Set", "AtCS", "menuIconKeys.png", "AddToCharacterSet", "mel", "")

        # Remove from Character Set
        self.setShelfButton("Remove highlighted Channel Box items to current character set", "Remove from Character Set", "RfCS", "menuIconKeys.png", "RemoveFromCharacterSet", "mel", "")

        # --------------------------------------------------------------------------------------------------
        # MUSCLE
        # --------------------------------------------------------------------------------------------------
        # Interactive Playback
        self.setShelfButton("Allows interaction with objects during playback", "Interactive Playback", "", "interactivePlayback.png", "InteractivePlayback", "mel", "")

        # Muscle Builder
        self.setShelfButton("Brings up a UI to build muscles and set their parameters.", "Muscle Builder...", "", "cMuscle_muscle_muscleBuilder.png", "cMuscleBuilder();", "mel", "")

        # Muscle Creator
        self.setShelfButton("Brings up the UI to create parametric muscles.", "Muscle Creator...", "", "cMuscle_muscle_creatorUI.png", "cMuscle_cMuscleCreatorUI();", "mel", "")

        # Convert Surface to Muscle/Bone
        self.setShelfButton("Converts selected objects to muscleObjects.", "Convert Surface to Muscle/Bone", "", "cMuscle_muscle_convertToMuscle.png", "cMuscle_makeMuscle(0);", "mel", "")

        # Connect Selected Muscle Objects
        self.setShelfButton("Connects selected cMuscleObject nodes to the selected muscleSystem deformer.", "Connect selected Muscle Objects", "", "cMuscle_skin_connMus.png", "cMuscle_connectToSystem();", "mel", "")

        # Paint Muscle Weights
        self.setShelfButton("Brings up the Artisan paint weights for the selected cMuscleSystem object.", "Paint Muscle Weights...", "", "cMuscle_skin_paint.png", "cMusclePaint(); ", "mel", "")

        # --------------------------------------------------------------------------------------------------
        # DEFORMERS
        # --------------------------------------------------------------------------------------------------
        # Wire Deformer
        self.setShelfButton("Select object(s), select curve(s)", "Wire", "", "wire.png", "WireTool", "mel", "")

        # Bend Deformer
        self.setShelfButton("Select items to deform", "Bend", "", "bendNLD.png", "Bend", "mel", "")

        # Sine Deformer
        self.setShelfButton("Select items to deform", "Sine", "", "sineNLD.png", "Sine", "mel", "")

        # Squash Deformer
        self.setShelfButton("Select items to deform", "Squash", "", "squashNLD.png", "Squash", "mel", "")

        # Twist Deformer
        self.setShelfButton("Select items to deform", "Twist", "", "twistNLD.png", "Twist", "mel", "")

        # Jiggle Deformer
        self.setShelfButton("Select object(s)", "Jiggle Deformer", "", "jiggleDeformer.png", "CreateJiggleDeformer", "mel", "")

        # --------------------------------------------------------------------------------------------------
        # OUTPUT
        # --------------------------------------------------------------------------------------------------
        # Playblast
        self.setShelfButton("Preview animation by screen-capturing frames", "Playblast", "", "playblast.png", "PlayblastWindow", "mel", "PlayblastOptions")

        # Bake Animation
        self.setShelfButton("Bake existing animation into keys", "Bake Animation", "", "bakeAnimation.png", r"doBakeSimulationArgList 7 { \"1\",\"0\",\"10\",\"1\",\"0\",\"0\",\"1\",\"1\",\"0\",\"1\",\"animationList\",\"0\",\"0\",\"0\",\"0\",\"0\",\"1\",\"0\" };", "mel", "BakeSimulationOptions")

        # Alembic Export
        self.setShelfButton("Export the selected objects to an Alembic file", "Export Selection to Alembic...", "EStA", "commandButton.png", r"doAlembicExportArgList 6 {\"0\",\"3\",\"1\",\"120\",\"1\",\"0\",\"-0.2\",\"0.2\",\"0\",\"0\",\"\",\"\",\"0\",\"1\",\"0\",\"0\",\"1\",\"0\",\"1\",\"0\",\"\",\"\",\"\",\"\",\"0\",\"0\",\"0\",\"2\",\"1\",\"0\"};", "mel", "AlembicExportSelectionOptions")

        # --------------------------------------------------------------------------------------------------
        # NODES
        # --------------------------------------------------------------------------------------------------
        # Blend Colors Node
        self.setShelfButton("Create BlendColors Node", "blendColors Node", "", "blendColors.svg", "cmds.shadingNode('blendColors', asUtility=True)", "python", "", 5, 5)

        # Condition Node
        self.setShelfButton("Create Condition Node", "condition Node", "", "condition.svg", "cmds.shadingNode('condition', asUtility=True)", "python", "", 5, 5)

        # Choice Node
        self.setShelfButton("Create Choice Node", "choice Node", "", "choice.svg", "cmds.shadingNode('choice', asUtility=True)", "python", "", 5, 5)

        # Plus Minus Average Node
        self.setShelfButton("Create PlusMinusAverage Node", "plusMinusAverage Node", "", "plusMinusAverage.svg", "cmds.shadingNode('plusMinusAverage', asUtility=True)", "python", "", 5, 5)

        # Multiply Divide Node
        self.setShelfButton("Create MultiplyDivide Node", "multiplyDivide Node", "", "multiplyDivide.svg", "cmds.shadingNode('multiplyDivide', asUtility=True)", "python", "", 5, 5)

        # Add Double Linear Node
        self.setShelfButton("Create AddDoubleLinear Node", "addDoubleLinear Node", "", "addDoubleLinear.svg", "cmds.shadingNode('addDoubleLinear', asUtility=True)", "python", "", 5, 5)

        # Mult Double Linear Node
        self.setShelfButton("Create MultDoubleLinear Node", "multDoubleLinear Node", "", "multDoubleLinear.svg", "cmds.shadingNode('multDoubleLinear', asUtility=True)", "python", "", 5, 5)

        # Distance Between Node
        self.setShelfButton("Create DistanceBetween Node", "distanceBetween Node", "", "distanceBetween.svg", "cmds.shadingNode('distanceBetween', asUtility=True)", "python", "", 5, 5)

        # Clamp Node
        self.setShelfButton("Create Clamp Node", "clamp Node", "", "clamp.svg", "cmds.shadingNode('clamp', asUtility=True)", "python", "", 5, 5)

        # Set Range Node
        self.setShelfButton("Create SetRange Node", "setRange Node", "", "setRange.svg", "cmds.shadingNode('setRange', asUtility=True)", "python", "", 5, 5)

        # Reverse Node
        self.setShelfButton("Create Reverse Node", "reverse Node", "", "reverse.svg", "cmds.shadingNode('reverse', asUtility=True)", "python", "", 5, 5)

        # Blend Two Attributes Node
        self.setShelfButton("Create BlendTwoAttr Node", "blendTwoAttr Node", "", "blendTwoAttr.svg", "cmds.shadingNode('blendTwoAttr', asUtility=True)", "python", "", 5, 5)

        # Curve Info Node
        self.setShelfButton("Create CurveInfo Node", "curveInfo Node", "", "curveInfo.svg", "cmds.shadingNode('curveInfo', asUtility=True)", "python", "", 5, 5)

        # Surface Info Node
        self.setShelfButton("Create SurfaceInfo Node", "surfaceInfo Node", "", "surfaceInfo.svg", "cmds.shadingNode('surfaceInfo', asUtility=True)", "python", "", 5, 5)

        # Remap Value Node
        self.setShelfButton("Create RemapValue Node", "remapValue Node", "", "remapValue.svg", "cmds.shadingNode('remapValue', asUtility=True)", "python", "", 5, 5)

        # Remap Color Node
        self.setShelfButton("Create RemapColor Node", "remapColor Node", "", "remapColor.svg", "cmds.shadingNode('remapColor', asUtility=True)", "python", "", 5, 5)

        # Angle Between Node
        self.setShelfButton("Create AngleBetween Node", "angleBetween Node", "", "angleDim.png", "cmds.shadingNode('angleBetween', asUtility=True)", "python", "", 5, 5)

        # Unit Conversion Node
        self.setShelfButton("Create UnitConversion Node", "unitConversion Node", "", "unitConversion.svg", "cmds.shadingNode('unitConversion', asUtility=True)", "python", "", 5, 5)

        # Add Matrix Node
        self.setShelfButton("Create AddMatrix Node", "addMatrix Node", "", "addMatrix.svg", "cmds.shadingNode('addMatrix', asUtility=True)", "python", "", 5, 5)

        # Decompose Matrix Node
        self.setShelfButton("Create DecomposeMatrix Node", "decomposeMatrix Node", "", "decomposeMatrix.svg", "cmds.shadingNode('decomposeMatrix', asUtility=True)", "python", "", 5, 5)

        # Vector Product Node
        self.setShelfButton("Create VectorProduct Node", "vectorProduct Node", "", "vectorProduct.svg", "cmds.shadingNode('vectorProduct', asUtility=True)", "python", "", 5, 5)

        # File Node
        self.setShelfButton("Create File Node", "file Node", "", "file.svg", "cmds.shadingNode('file', asTexture=True)", "python", self.connectPlace2dTexture("file"), 5, 5)

        # Ramp Node
        self.setShelfButton("Create Ramp Node", "ramp Node", "", "ramp.svg", "cmds.shadingNode('ramp', asTexture=True)", "python", self.connectPlace2dTexture("ramp"), 5, 5)

        # Checker Node
        self.setShelfButton("Create Checker Node", "checker Node", "", "checker.svg", "cmds.shadingNode('checker', asTexture=True)", "python", self.connectPlace2dTexture("checker"), 5, 5)

        # Noise Node
        self.setShelfButton("Create Noise Node", "noise Node", "", "solidFractal.svg", "cmds.shadingNode('noise', asTexture=True)", "python", self.connectPlace2dTexture("noise"), 5, 5)

    def setShelfButton(self, annotation, label, imageLabel, icon, command, cmdType, double, maw=0, mah=0):
        finalCommand = ""
        ecr = 'enableCommandRepeat=True'
        en = 'en=True'
        w = 'w=35'
        h = 'h=35'
        m = 'm=True'
        vis = 'vis=True'
        po = 'po=False'
        ann = ('ann="'+annotation+'"')
        eb = 'enableBackground=False'
        al = 'al="center"'
        l = ('l="'+label+'"')
        lo = 'lo=0'
        ua = 'useAlpha=True'
        font = 'font="plainLabelFont"'
        iol = ('iol="'+imageLabel+'"')
        olc = 'overlayLabelColor=(0.8, 0.8, 0.8)'
        olb = 'overlayLabelBackColor=(0, 0, 0, 0.5)'
        i = ('i="'+icon+'"')
        i1 = ('i1="'+icon+'"')
        st = 'st="iconOnly"'
        # mw = ('mw="'+str(maw)+'"')
        # mh = ('mh="'+str(mah)+'"')
        c = ('c="'+command+'"')
        stp = ('stp="'+cmdType+'"')
        rpt = 'rpt=True'
        dcc = ('dcc="'+double+'"')
        fl = 'flat=True'

        finalCommand = 'cmds.shelfButton('+ecr+', '+en+', '+w+', '+h+', '+m+', '+vis+', '+po+', '+ann+', '+eb+', '+al+', '+l+', '+lo+', '+ua+', '+font+', '+iol+', '+olc+', '+olb+', '+i+', '+i1+', '+st+', mw='+str(maw)+', mh='+str(mah)+', '+c+', '+stp+', '+rpt+', '+dcc+', '+fl+')'
        exec(finalCommand)

    def connectPlace2dTexture(self, outNode):
        command = []
        finalCommand = ''
        if outNode == "file":
            command.append("node = cmds.shadingNode('file', asTexture=True);")
            command.append("place = cmds.shadingNode('place2dTexture', asUtility=True);")
            command.append("cmds.connectAttr(place+'.coverage', node+'.coverage');")
            command.append("cmds.connectAttr(place+'.translateFrame', node+'.translateFrame');")
            command.append("cmds.connectAttr(place+'.rotateFrame', node+'.rotateFrame');")
            command.append("cmds.connectAttr(place+'.mirrorU', node+'.mirrorU');")
            command.append("cmds.connectAttr(place+'.mirrorV', node+'.mirrorV');")
            command.append("cmds.connectAttr(place+'.stagger', node+'.stagger');")
            command.append("cmds.connectAttr(place+'.wrapU', node+'.wrapU');")
            command.append("cmds.connectAttr(place+'.wrapV', node+'.wrapV');")
            command.append("cmds.connectAttr(place+'.repeatUV', node+'.repeatUV');")
            command.append("cmds.connectAttr(place+'.offset', node+'.offset');")
            command.append("cmds.connectAttr(place+'.rotateUV', node+'.rotateUV');")
            command.append("cmds.connectAttr(place+'.noiseUV', node+'.noiseUV');")
            command.append("cmds.connectAttr(place+'.vertexUvOne', node+'.vertexUvOne');")
            command.append("cmds.connectAttr(place+'.vertexUvTwo', node+'.vertexUvTwo');")
            command.append("cmds.connectAttr(place+'.vertexUvThree', node+'.vertexUvThree');")
            command.append("cmds.connectAttr(place+'.vertexCameraOne', node+'.vertexCameraOne');")
            command.append("cmds.connectAttr(place+'.outUV', node+'.uv');")
            command.append("cmds.connectAttr(place+'.outUvFilterSize', node+'.uvFilterSize')")
            finalCommand = ''.join(command)
            return finalCommand
        elif outNode == "ramp":
            command.append("node = cmds.shadingNode('ramp', asTexture=True);")
            command.append("place = cmds.shadingNode('place2dTexture', asUtility=True);")
            command.append("cmds.connectAttr(place+'.outUV', node+'.uv');")
            command.append("cmds.connectAttr(place+'.outUvFilterSize', node+'.uvFilterSize')")
            finalCommand = ''.join(command)
            return finalCommand
        elif outNode == "checker":
            command.append("node = cmds.shadingNode('checker', asTexture=True);")
            command.append("place = cmds.shadingNode('place2dTexture', asUtility=True);")
            command.append("cmds.connectAttr(place+'.outUV', node+'.uv');")
            command.append("cmds.connectAttr(place+'.outUvFilterSize', node+'.uvFilterSize')")
            finalCommand = ''.join(command)
            return finalCommand
        elif outNode == "noise":
            command.append("node = cmds.shadingNode('noise', asTexture=True);")
            command.append("place = cmds.shadingNode('place2dTexture', asUtility=True);")
            command.append("cmds.connectAttr(place+'.outUV', node+'.uv');")
            command.append("cmds.connectAttr(place+'.outUvFilterSize', node+'.uvFilterSize')")
            finalCommand = ''.join(command)
            return finalCommand
        else: return "return False"
