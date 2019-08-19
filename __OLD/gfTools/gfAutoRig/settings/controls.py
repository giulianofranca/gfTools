import maya.cmds as cmds


class Control(object):

    def __init__(self, n, t, s, c=None):
        self.type = t
        self.name = n
        self.size = s
        self.color = 0
        # Colors
        if c == "Red": self.color = 13
        elif c == "DarkRed": self.color = 4
        elif c == "LightRed": self.color = 20
        elif c == "Blue": self.color = 6
        elif c == "DarkBlue": self.color = 29 # OLD: 15
        elif c == "LightBlue": self.color = 18
        elif c == "Yellow": self.color = 17
        elif c == "DarkYellow": self.color = 24
        elif c == "LightYellow": self.color = 25
        elif c == "DarkGreen": self.color = 23
        elif c == "Purple": self.color = 30
        elif c == "Magenta": self.color = 31
        # Edited colors
        elif c == 'Primary': self.color = 22    # Yellow
        elif c == 'Secondary': self.color = 20  # Pink
        elif c == 'Tertiary': self.color = 29   # Blue
        elif c == 'Global': self.color = 30     # Purple
        elif c == 'Extra': self.color = 1       # Black
        # Types
        if self.type == "Circle": self._Circle()
        elif self.type == "Box": self._Box()
        elif self.type == "Global": self._Global()
        elif self.type == "Track": self._Track()
        elif self.type == "Diamond": self._Diamond()
        elif self.type == "Gear": self._Gear()
        elif self.type == "Gear Smooth": self._GearSmooth()
        elif self.type == "Root": self._Root()
        elif self.type == "Hip": self._Hip()
        elif self.type == "Chest": self._Chest()
        elif self.type == "Foot": self._Foot()
        elif self.type == "Hand": self._Hand()
        elif self.type == "Head": self._Head()
        elif self.type == "IKFKSwitch": self._IKFKSwitch()
        elif self.type == "Lock and Hide": self._LockAndHide()

    def __repr__(self):
        return self.name

    def __str__(self):
        return str(self.name)

    def _LockAndHide(self):
        for attr in self.size:
            cmds.setAttr((self.name+"."+attr), lock=True, keyable=False, channelBox=False)

    def _Circle(self):
        ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01)
        cmds.setAttr((ctrl[0]+".sx"), 12)
        cmds.setAttr((ctrl[0]+".sy"), 12)
        cmds.setAttr((ctrl[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        ctrlShapes = cmds.listRelatives(ctrl[0], s=True)
        for sh in ctrlShapes:
            cmds.setAttr((sh+".overrideEnabled"), 1)
            cmds.setAttr((sh+".overrideColor"), self.color)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.rename(ctrl[0], self.name)

    def _Box(self):
        ctrl = cmds.curve(d=1, p=[(-12.06, 12.06, 12.06), (-12.06, -12.06, 12.06), (12.06, -12.06, 12.06),
            (12.06, 12.06, 12.06), (-12.06, 12.06, 12.06), (-12.06, 12.06, -12.06), (12.06, 12.06, -12.06),
            (12.06, 12.06, 12.06), (12.06, -12.06, 12.06), (12.06, -12.06, -12.06), (12.06, 12.06, -12.06),
            (-12.06, 12.06, -12.06), (-12.06, -12.06, -12.06), (12.06, -12.06, -12.06), (12.06, -12.06, 12.06),
            (-12.06, -12.06, 12.06), (-12.06, -12.06, -12.06)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13,
            14, 15, 16])
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        ctrlShapes = cmds.listRelatives(ctrl, s=True)
        for sh in ctrlShapes:
            cmds.setAttr((sh+".overrideEnabled"), 1)
            cmds.setAttr((sh+".overrideColor"), self.color)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Global(self):
        ctrl = cmds.curve(d=1, p=[(0.0, 0.0, 12.06), (6.03, 0.0, 9.04), (3.01, 0.0, 9.04),
            (3.01, 0.0, 6.03), (4.51, 0.0, 4.51), (6.03, 0.0, 3.01), (9.04, 0.0, 3.01),
            (9.04, 0.0, 6.03), (12.06, 0.0, 0.0), (9.04, 0.0, -6.03), (9.04, 0.0, -3.01),
            (6.03, 0.0, -3.01), (4.51, 0.0, -4.51), (3.01, 0.0, -6.03), (3.01, 0.0, -9.04),
            (6.03, 0.0, -9.04), (0.0, 0.0, -12.06), (-6.03, 0.0, -9.04), (-3.01, 0.0, -9.04),
            (-3.01, 0.0, -6.03), (-4.51, 0.0, -4.51), (-6.03, 0.0, -3.01), (-9.04, 0.0, -3.01),
            (-9.04, 0.0, -6.03), (-12.06, 0.0, 0.0), (-9.04, 0.0, 6.03), (-9.04, 0.0, 3.01),
            (-6.03, 0.0, 3.01), (-4.51, 0.0, 4.51), (-3.01, 0.0, 6.03), (-3.01, 0.0, 9.04),
            (-6.03, 0.0, 9.04), (0.0, 0.0, 12.06)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11,
            12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32])
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl+".overrideEnabled"), 1)
        cmds.setAttr((ctrl+".overrideColor"), self.color)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Track(self):
        ctrl = cmds.curve(d=1, p=[(0.0, 0.0, 2.6), (8.30, 0.0, 8.3), (2.6, 0.0, 0.0), (8.3, 0.0, -8.3),
            (0.0, 0.0, -2.6), (-8.3, 0.0, -8.3), (-2.6, 0.0, 0.0), (-8.3, 0.0, 8.3),
            (0.0, 0.0, 2.6)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl+".overrideEnabled"), 1)
        cmds.setAttr((ctrl+".overrideColor"), self.color)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Diamond(self):
        ctrl = cmds.curve(d=1, p=[(0, 11.6, 0), (0, 0, -11.6), (0, -11.6, 0), (0, 0, 11.6), (0, 11.6, 0),
           (-11.6, 0, 0), (0, -11.6, 0), (11.6, 0, 0), (0, 11.6, 0), (0, 0, -11.6), (11.6, 0, 0),
           (0, 0, 11.6), (-11.6, 0, 0), (0, 0, -11.6)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        cmds.select(ctrl, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl+".overrideEnabled"), 1)
        cmds.setAttr((ctrl+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Gear(self):
        ctrl1 = cmds.curve(d=1, p=[(0, 0, 10.6), (-4.07, 0, 9.8), (-5.08, 0, 12.28), (-9.4, 0, 9.4), (-7.5, 0, 7.5), (-9.8, 0, 4.07),
           (-12.2, 0, 5.08), (-13.2, 0, 0), (-10.6, 0, 0), (-9.8, 0, -4.07), (-12.28, 0, -5.08), (-9.4, 0, -9.4),
           (-7.5, 0, -7.5), (-4.07, 0, -9.8), (-5.08, 0, -12.28), (0, 0, -13.29), (0, 0, -10.63), (4.07, 0, -9.82),
           (5.08, 0, -12.28),(9.4, 0, -9.4), (7.52, 0, -7.52), (9.82, 0, -4.07), (12.28, 0, -5.08), (13.29, 0, 0),
           (10.63, 0, 0), (9.82, 0, 4.07), (12.28, 0, 5.08), (9.4, 0, 9.4), (7.5, 0, 7.5),(4.07, 0, 9.82),
           (5.08, 0, 12.28), (0, 0, 13.29), (0, 0, 10.63)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,
               16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28,29, 30, 31, 32])
        ctrl2 = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01)
        cmds.setAttr((ctrl2[0]+".sx"), 12)
        cmds.setAttr((ctrl2[0]+".sy"), 12)
        cmds.setAttr((ctrl2[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.setAttr((ctrl2[0]+".sx"), 0.6)
        cmds.setAttr((ctrl2[0]+".sy"), 0.6)
        cmds.setAttr((ctrl2[0]+".sz"), 0.6)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.select(ctrl2[0], r=True)
        cmds.pickWalk(d="down")
        cmds.select(ctrl1, add=True)
        cmds.parent(r=True, s=True)
        cmds.select(ctrl2[0], r=True)
        cmds.Delete()
        cmds.select(ctrl1, r=True)
        cmds.rotate(0, 11.5, 0, r=True, os=True, fo=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl1+".overrideEnabled"), 1)
        cmds.setAttr((ctrl1+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(ctrl1, self.name)

    def _GearSmooth(self):
        crv = cmds.circle(d=3, nr=(0, 1, 0), c=(0, 0, 0), s=16)
        cmds.setAttr((crv[0]+".sx"), 12)
        cmds.setAttr((crv[0]+".sy"), 12)
        cmds.setAttr((crv[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cvs = []
        for x in range(0,16):
            if x % 2 != 0: cvs.append(x)
        sel = []
        for eachCv in cvs:
            sel.append(crv[0]+".cv["+str(eachCv)+"]")
        cmds.select(sel, r=True)
        cmds.scale(0.4, 0.4, 0.4, r=True)
        cmds.select(crv[0], r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.scale(1.25, 1.25, 1.25, r=True, os=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((crv[0]+".overrideEnabled"), 1)
        cmds.setAttr((crv[0]+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(crv[0], self.name)

    def _Root(self):
        ctrl = cmds.curve(d=1, p=[(11.03, 2.55, 9.22), (12.52, -2.55, 10.54), (12.52, -2.55, -11.39),
            (11.03, 2.55, -10.07), (-10.63, 2.55, -10.07), (-12.12, -2.55, -11.40),
            (-12.12, -2.55, 10.54), (-10.63, 2.55, 9.22), (11.03, 2.55, 9.22),
            (11.03, 2.55, -10.07), (12.52, -2.55, -11.40), (-12.12, -2.55, -11.40),
            (-10.63, 2.55, -10.07), (-10.63, 2.55, 9.22), (-12.12, -2.55, 10.54),
            (12.52, -2.55, 10.54)], k=[0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15])
        cmds.select(ctrl, r=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl+".overrideEnabled"), 1)
        cmds.setAttr((ctrl+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Hip(self):
        ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01)
        cmds.setAttr((ctrl[0]+".sx"), 12)
        cmds.setAttr((ctrl[0]+".sy"), 12)
        cmds.setAttr((ctrl[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.select((ctrl[0]+".cv[3]"), (ctrl[0]+".cv[7]"), r=True)
        cmds.move(0, 0.605, -0.97, r=True, os=True)
        cmds.select((ctrl[0]+".cv[4]"), (ctrl[0]+".cv[6]"), r=True)
        cmds.move(0, 3.87, -1.93, r=True, os=True)
        cmds.select((ctrl[0]+".cv[0]"), (ctrl[0]+".cv[2]"), r=True)
        cmds.move(0, 3.87, 0, r=True, os=True)
        cmds.select((ctrl[0]+".cv[5]"),r=True)
        cmds.move(0, -8.045, -3.92, r=True, os=True)
        cmds.select((ctrl[0]+".cv[1]"),r=True)
        cmds.move(0, -8.045, 1.641, r=True, os=True)
        cmds.select(ctrl[0], r=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl[0]+".overrideEnabled"), 1)
        cmds.setAttr((ctrl[0]+".overrideColor"), self.color)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.rename(ctrl[0], self.name)

    def _Chest(self):
        ctrl = cmds.curve(d=1, p=[(0.0, 0.80, 11.80), (9.43, 2.18, 6.28), (9.43, -2.18, -2.64),
            (9.43, 2.18, -8.14), (0.0, 0.80, -11.80), (-9.42, 2.18, -8.14),
            (-9.43, -2.18, -2.64), (-9.43, 2.18, 6.28), (0.0, 0.80, 11.80)],
            k=[0, 1, 2, 3, 4, 5, 6, 7, 8])
        cmds.select(ctrl, r=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl+".overrideEnabled"), 1)
        cmds.setAttr((ctrl+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(ctrl, self.name)

    def _Foot(self):
        ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01)
        cmds.setAttr((ctrl[0]+".sx"), 12)
        cmds.setAttr((ctrl[0]+".sy"), 12)
        cmds.setAttr((ctrl[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.setAttr(ctrl[0]+".sx", 1.5)
        cmds.setAttr(ctrl[0]+".sy", 1.5)
        cmds.setAttr(ctrl[0]+".sz", 1.5)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.select(ctrl[0]+".cv[2]", ctrl[0]+".cv[0]", r=True)
        cmds.scale(0.61, 1, 1, p=(0, 0, -13.16), r=True)
        cmds.select(ctrl[0]+".cv[3]", ctrl[0]+".cv[7]", r=True)
        cmds.scale(0.2, 1, 1, p=(0, 0, 0), r=True)
        cmds.move(3.4, 0, 0, r=True)
        cmds.select(ctrl[0]+".cv[4:6]", r=True)
        cmds.move(0, 0, 4.27, r=True)
        cmds.select(ctrl[0]+".cv[3]", ctrl[0]+".cv[7]", r=True)
        cmds.move(0, 3.82, 0, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.select(ctrl[0], r=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.CenterPivot()
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.DeleteHistory()
        cmds.CenterPivot()
        cmds.setAttr((ctrl[0]+".overrideEnabled"), 1)
        cmds.setAttr((ctrl[0]+".overrideColor"), self.color)
        cmds.select(ctrl[0], r=True)
        cmds.rename(ctrl[0], self.name)

    def _Hand(self):
        ctrl = cmds.circle(c=(0, 0, 0), nr=(0, 1, 0), sw=360, r=12, d=3, ut=0, tol=0.01, s=8, ch=False)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.CenterPivot()
        cmds.DeleteHistory()
        cmds.setAttr(ctrl[0]+'.s', 1.3, 1.3, 1.3)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.move(-13.926404, 0, -6.963202, ctrl[0]+'.cv[6]', r=True)
        cmds.move(0, 0, 9.209396, ctrl[0]+'.cv[7]', r=True)
        cmds.move(10.107874, 0, -1.796955, ctrl[0]+'.cv[5]', r=True)
        cmds.move(0, 0, 3.81853, ctrl[0]+'.cv[1]', r=True)
        cmds.move(-2.470814, 0, 0, ctrl[0]+'.cv[2]', r=True)
        cmds.move(-4.168159, 0, -2.74221, ctrl[0]+'.cv[6]', r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.scale(self.size, self.size, self.size, ctrl[0], r=True)
        cmds.move(-16, 0, 0, ctrl[0]+'.sp', ctrl[0]+'.rp', rpr=True)
        cmds.move(16, 0, 0, ctrl[0], r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=False, pn=True)
        cmds.DeleteHistory()
        cmds.setAttr(ctrl[0]+'.overrideEnabled', True)
        cmds.setAttr(ctrl[0]+'.overrideColor', self.color)
        cmds.rename(ctrl[0], self.name)

    def _Head(self):
        ctrl = cmds.circle(nr=(0, 1, 0), c=(0, 0, 0), sw=360, r=1, d=3, ut=0, tol=0.01)
        cmds.setAttr((ctrl[0]+".sx"), 12)
        cmds.setAttr((ctrl[0]+".sy"), 12)
        cmds.setAttr((ctrl[0]+".sz"), 12)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.move(34.17, 0, 0, (ctrl[0]+".cv[0]"), (ctrl[0]+".cv[6:7]"), r=True, os=True)
        cmds.scale(1, 1, 2.29, (ctrl[0]+".cv[0]"), (ctrl[0]+".cv[6]"), r=True)
        cmds.move(15.1, 0, 0, (ctrl[0]+".cv[1]"), (ctrl[0]+".cv[5]"), r=True, os=True)
        cmds.scale(1, 1, 1.37, (ctrl[0]+".cv[1]"), (ctrl[0]+".cv[5]"), r=True)
        cmds.move(10.21, 0, 0, (ctrl[0]+".cv[2:4]"), r=True, os=True)
        cmds.scale(1, 1, 1.37, (ctrl[0]+".cv[2]"), (ctrl[0]+".cv[4]"), r=True)
        cmds.select(ctrl[0], r=True)
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
        cmds.setAttr((ctrl[0]+".overrideEnabled"), 1)
        cmds.setAttr((ctrl[0]+".overrideColor"), self.color)
        cmds.DeleteHistory()
        cmds.rename(ctrl[0], self.name)

    def _IKFKSwitch(self):
        txt = cmds.textCurves(ch=False, f="Arial|wt:50|sz:150|sl:n|st:100", t="IK/FK")
        children = cmds.listRelatives(c=True)
        cmds.select(hi=True)
        crvs = cmds.ls("*curve*", sl=True, type="transform")
        crvsSh = cmds.ls(sl=True, type="curveShape")
        x = len(crvsSh) - 1
        cmds.select(hi=True)
        for c in crvs:
            cmds.parent(crvs[x], txt)
            cmds.select(crvs[x], r=True)
            cmds.makeIdentity(apply=True, t=True, r=True, s=True, n=0, pn=True)
            if x > 0:
                cmds.parent(crvsSh[x], crvs[0], r=True, s=True)
            x -= 1
        cmds.parent(crvs[0], w=True)
        cmds.select(txt, r=True)
        cmds.Delete()
        cmds.select(crvs[0])
        cmds.scale(self.size, self.size, self.size, r=True)
        cmds.rename(crvs[0], self.name)
        childs = cmds.listRelatives(s=True)
        for child in childs:
            cmds.setAttr((child+".overrideEnabled"), 1)
            cmds.setAttr((child+".overrideColor"), self.color)
            cmds.rename(child, ("Crv_Shape_1"))
