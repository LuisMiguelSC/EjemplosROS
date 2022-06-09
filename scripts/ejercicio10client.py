#!/usr/bin/env python
from cmath import pi
import rospy
import sys
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove3, InitiateMove3Request, InitiateMove3Response

def usage():
    return '%s [Lado poligono (longitud)] [Lados del polígono]' % sys.argv[0]

if __name__ == '__main__':
    if len(sys.argv) >= 3:
        distance = float(sys.argv[1])
        n = float(sys.argv[2])
        if n < 3:
            print('Un polígono debe tener 3 lados o más')
            sys.exit(1)
    else:
        print(usage())
        sys.exit(1)  
    print('Pidiendo polígono de '+ str(n) + ' lados de longitud '+ str(distance))
    lado = 1
    while lado < n+1:
        rospy.wait_for_service('move')
        try:
            move = rospy.ServiceProxy('move', InitiateMove3)
            if lado != 1:
                resp: InitiateMove3Response = move(1,360/n)         
            resp: InitiateMove3Response = move(0,distance)
            if resp.respuesta == 1:
                print('Lado '+ str(lado))
            else:
                print('Parece ser que no se ha podido realizar el movimiento lineal del lado ' +str(lado))
                sys.exit(1)
            lado = lado +1
            if lado == n+1:
                resp: InitiateMove3Response = move(1,360/n)   
                if resp.respuesta == 1:
                    print('Polígono terminado')
        except rospy.ServiceException as e:
            print('Service call failed: %s' % e)