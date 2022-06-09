#!/usr/bin/env python
from cmath import pi
import rospy
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove2, InitiateMove2Request, InitiateMove2Response

# Se usa el servidor del ejercicio 4 (que es igual al ejercicio 5, ya que ya estaba usando el feedback...)
def usage():
    return '%s [Lado poligono (longitud)] [Lados del polígono]' % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) == 3:
        distance = int(sys.argv[1])
        n = int(sys.argv[2])
        if n < 3:
            print('Un polígino debe tener 3 lados o más')
            sys.exit(1)
    else:
        print(usage())
        sys.exit(1)  
    print('Pidiendo polígono de '+ str(n) + ' lados de longitud '+ str(distance))
    lado = 1
    while lado < n+1:
        rospy.wait_for_service('move')
        try:
            move = rospy.ServiceProxy('move', InitiateMove2)
            if lado != 1:
                resp: InitiateMove2Response = move(1,round(360/n))         
            resp: InitiateMove2Response = move(0,distance)
            if resp.respuesta == 1:
                print('Lado '+ str(lado))
            lado = lado +1
            if lado == n+1:
                resp: InitiateMove2Response = move(1,round(360/n))   
                if resp.respuesta == 1:
                    print('Polígono terminado')
        except rospy.ServiceException as e:
            print('Service call failed: %s' % e)