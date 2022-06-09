#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sanchezcorralluismiguel.srv import InitiateMove, InitiateMoveRequest, InitiateMoveResponse

def mueveRobot(req):
    terminado = 0
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    posicion_inicialx = posicionx

    if req.iniciar != 0:
        rospy.sleep(2)
        rospy.loginfo('Iniciando movimiento')
        msg = Twist()
        msg.linear.x = 0.05 # m/s
        pub.publish(msg)
    else:
        terminado =1
    while terminado!=1:
        if abs(posicionx-posicion_inicialx) > 1:
            msg.linear.x = 0.0
            pub.publish(msg)
            terminado = 1
            rospy.loginfo('Posicion inicial: ' + str(posicion_inicialx) + ', Posición final: '+ str(posicionx))
            return InitiateMoveResponse(1)

def get_position(msg: Odometry):
    global posicionx
    posicionx = msg.pose.pose.position.x
    #rospy.loginfo('Posicion: ' + str(posicionx))

if __name__ == '__main__':
    sub = rospy.Subscriber('/odom', Odometry, get_position)
    rospy.init_node('moverseservidor')
    s = rospy.Service('move', InitiateMove, mueveRobot)
    rospy.loginfo("Ready to move.")
    rospy.spin()