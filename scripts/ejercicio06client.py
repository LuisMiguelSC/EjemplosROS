#!/usr/bin/env python
from cmath import pi
import rospy
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove2, InitiateMove2Request, InitiateMove2Response

# Se usa el servidor del ejercicio 4 (que es igual al ejercicio 5, ya que ya estaba usando el feedback...)
def usage():
    return '%s [Lado triangulo]' % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) == 2:
        distance = int(sys.argv[1])
    else:
        print(usage())
        sys.exit(1)
    print('Pidiendo triangulo')
    lado = 1
    while lado < 4:
        rospy.wait_for_service('move')
        try:
            move = rospy.ServiceProxy('move', InitiateMove2)
            if lado != 1:
                resp: InitiateMove2Response = move(1,180-60)         
            resp: InitiateMove2Response = move(0,distance)
            if resp.respuesta == 1:
                print('Lado '+ str(lado))
            lado = lado +1
            if lado == 4:
                resp: InitiateMove2Response = move(1,180-60)   
                if resp.respuesta == 1:
                    print('Triángulo terminado')
        except rospy.ServiceException as e:
            print('Service call failed: %s' % e)