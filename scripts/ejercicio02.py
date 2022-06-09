#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry

def mueveRobot():
    terminado = 0
    rospy.init_node('ejercicio2', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    posicion_inicialx = posicionx

    rospy.sleep(2)
    rospy.loginfo('Iniciando movimiento')
    msg = Twist()
    msg.linear.x = 0.05 # m/s
    pub.publish(msg)

    while terminado!=1:
        if abs(posicionx-posicion_inicialx) > 1:
            msg.linear.x = 0.0
            pub.publish(msg)
            terminado = 1
            rospy.loginfo('Posicion inicial: ' + str(posicion_inicialx) + ', Posición final: '+ str(posicionx))

def get_position(msg: Odometry):
    global posicionx
    posicionx = msg.pose.pose.position.x
    #rospy.loginfo('Posicion: ' + str(posicionx))

if __name__ == '__main__':
    sub = rospy.Subscriber('/odom', Odometry, get_position)
    try:
        mueveRobot()
    except rospy.ROSInterruptException:
        pass
