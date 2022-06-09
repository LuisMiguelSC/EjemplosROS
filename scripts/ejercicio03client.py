#!/usr/bin/env python
import rospy
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove, InitiateMoveRequest, InitiateMoveResponse

def usage():
    return '%s [1]' % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        request = int(sys.argv[1])
    else:
        print(usage())
        sys.exit(1)
    print('Pidiendo movimiento')
    rospy.wait_for_service('move')
    try:
        move = rospy.ServiceProxy('move', InitiateMove)
        resp: InitiateMoveResponse = move(request)
        if resp.respuesta == 1:
            print('Movimiento realizado')
    except rospy.ServiceException as e:
        print('Service call failed: %s' % e)