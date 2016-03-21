import random
class Arm:
    def __init__(self, position):
        self.position = position

    def action(self, action, dist_x, dist_y, arm_id):
	#Depending on Actions #Position [y][x][z]
        #Rotate base anti-clockwise
	unit = 30
        if arm_id == 1:
	    if action == 0:
                for i in xrange(len(self.position[0])):
		    self.position[i][2] -= unit
	        return 0
	#Rotate base clockwise
	    if action == 1:
                for i in xrange(len(self.position[0])):
                    self.position[i][2] += unit
	        return 0
        #Shoulder up
	    if action == 2:
	        self.position[0][0] -= dist_y
	        self.position[0][1] -= dist_x
                self.position[1][0] -= dist_y
                self.position[1][1] -= dist_x
	        return 0
        #Shoulder down
	    if action == 3:
                self.position[0][0] += dist_y
                self.position[0][1] += dist_x
                self.position[1][0] += dist_y
                self.position[1][1] += dist_x
	        return 0
        #Elbow up
	    if action == 4:
                self.position[1][0] -= dist_y
                self.position[1][1] -= dist_x
                self.position[2][0] -= dist_y
                self.position[2][1] -= dist_x
	        return 0
        #Elbow down
	    if action == 5:
                self.position[1][0] += dist_y
                self.position[1][1] += dist_x
                self.position[2][0] += dist_y
                self.position[2][1] += dist_x
	        return 0
        #Wrist up
            if action == 6:
                self.position[2][0] -= dist_y
                self.position[2][1] -= dist_x
	        return 0
        # Wrist down
            if action == 7:
                self.position[2][0] += dist_y
                self.position[2][1] += dist_x
	        return 0
        #Grip open
        #Grip close
	if arm_id == 2:
	    if action == 0:
                for i in xrange(len(self.position[0])):
		    self.position[i][2] -= unit
	        return 0
	#Rotate base clockwise
	    if action == 1:
                for i in xrange(len(self.position[0])):
                    self.position[i][2] += unit
	        return 0
        #Shoulder up
	    if action == 2:
	        self.position[0][0] -= dist_y
	        self.position[0][1] += dist_x
                self.position[1][0] -= dist_y
                self.position[1][1] += dist_x
	        return 0
        #Shoulder down
	    if action == 3:
                self.position[0][0] += dist_y
                self.position[0][1] -= dist_x
                self.position[1][0] += dist_y
                self.position[1][1] -= dist_x
	        return 0
        #Elbow up
	    if action == 4:
                self.position[1][0] -= dist_y
                self.position[1][1] += dist_x
                self.position[2][0] -= dist_y
                self.position[2][1] += dist_x
	        return 0
        #Elbow down
	    if action == 5:
                self.position[1][0] += dist_y
                self.position[1][1] -= dist_x
                self.position[2][0] += dist_y
                self.position[2][1] -= dist_x
	        return 0
        #Wrist up
            if action == 6:
                self.position[2][0] -= dist_y
                self.position[2][1] += dist_x
	        return 0
        # Wrist down
            if action == 7:
                self.position[2][0] += dist_y
                self.position[2][1] -= dist_x
	        return 0
        #Grip open
	    if action == 8:
                self.position[2][0] -= dist_y
                self.position[2][1] += dist_x
                return 0
        #Grip close
            if action == 9:
                self.position[2][0] += dist_y
                self.position[2][1] -= dist_x
                return 0
        #Restart Position
	
    def limit_position(self, arm_id):
	if arm_id == 1:
	    self.position = (100, 100, 100)
	if arm_id == 2:
	    self.position = (100, 100, 100)

    def set_random_position(self, arm_id):
        if arm_id == 1:
            ux1 = random.randint(50, 200)
	    ux2 = random.randint(200, 350) 
	    ux3 = random.randint(350, 500)

	    uy1 = ux1-10
	    uy2 = ux2-120
	    uy3 = ux3-250

            self.position = ([uy1, ux1, 0], [uy2, ux2, 0], [uy3, ux3, 0])
	    return 0

        if arm_id == 2:
            ux1 = random.randint(850, 900)
            ux2 = random.randint(750, 800)
            ux3 = random.randint(650, 750)

            uy1 = -ux1+900
            uy2 = -ux2+900
            uy3 = -ux3+900

            self.position = ([uy1, ux1, 0], [uy2, ux2, 0], [uy3, ux3, 0])
            return 0


    def get_positions(self):
	return self.position
