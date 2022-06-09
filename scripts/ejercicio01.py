#!/usr/bin/env python
import rospy
from geometry_msgs.msg import Twist

def mueveRobot():
    rospy.init_node('ejercicio1', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)

    rospy.sleep(2)
    rospy.loginfo('Iniciando movimiento')
    msg = Twist()
    msg.linear.x = 0.05 # m/s
    pub.publish(msg)

    rospy.sleep(20)

    msg.linear.x = 0.0
    pub.publish(msg)

   

if __name__ == '__main__':
    try:
        mueveRobot()
    except rospy.ROSInterruptException:
        pass
