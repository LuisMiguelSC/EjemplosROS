#!/usr/bin/env python
from cmath import pi
import rospy
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove2, InitiateMove2Request, InitiateMove2Response

def usage():
    return '%s [0,1] (Lineal, Rotacion) [Longitud/Angulo]' % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) == 3:
        request = int(sys.argv[1])
        distance = int(sys.argv[2]) 
    else:
        print(usage())
        sys.exit(1)
    print('Pidiendo movimiento')
    rospy.wait_for_service('move')
    try:
        move = rospy.ServiceProxy('move', InitiateMove2)
        resp: InitiateMove2Response = move(request,distance)
        if resp.respuesta == 1:
            print('Movimiento realizado')
    except rospy.ServiceException as e:
        print('Service call failed: %s' % e)