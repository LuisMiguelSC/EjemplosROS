#!/usr/bin/env python
from cmath import cos, pi , sqrt    
import rospy
import math
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from sanchezcorralluismiguel.srv import InitiateMove2, InitiateMove2Request, InitiateMove2Response
from tf.transformations import euler_from_quaternion, quaternion_from_euler

# Este script se utiliza con ejercicio07client

def mueveRobot(req):
    terminado = 0
    pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
    posicion_inicialx = posicionx
    posicion_inicialy = posiciony
    yaw_inicial = yaw
    yaw_anterior = yaw_inicial
    cambiosigno = 0
    obstaculo_actual = obstaculo

    if req.tipo == 0: # Movimiento lineal
        rospy.sleep(2)
        rospy.loginfo('Iniciando movimiento lineal')
        msg = Twist()
        msg.linear.x = 0.13# m/s
        pub.publish(msg)
        while terminado!=1:
            if obstaculo_actual < req.longitud+0.2: # Dejo un márgen de seguridad
                msg.linear.x = 0.0
                pub.publish(msg)
                terminado = 1
                rospy.loginfo('No se ha podido realizar el movimiento pues había un obstáculo')
                return InitiateMove2Response(0)
            rospy.loginfo('Posicion inicial (X,Y): (' + str(posicion_inicialx) +',' + str(posicion_inicialy) + '), Posición (X,Y): '+ str(posicionx)+',' + str(posiciony))
            if abs(sqrt((posicionx-posicion_inicialx)**2 + (posiciony-posicion_inicialy)**2)) > req.longitud: # Veo si he llegado al destino              
                msg.linear.x = 0.0
                pub.publish(msg)
                terminado = 1
                rospy.loginfo('Posicion inicial (X,Y): (' + str(posicion_inicialx) +',' + str(posicion_inicialy) + '), Posición final (X,Y): '+ str(posicionx)+',' + str(posiciony))
                return InitiateMove2Response(1)
    elif req.tipo ==1: # Movimiento rotacional
        rospy.sleep(2)
        rospy.loginfo('Iniciando movimiento rotacional')
        msg = Twist()
        command.angular.z = 0.15 # rad/s
        pub.publish(command)
        while terminado!=1:
            rospy.loginfo('Angulo inicial: ' + str(yaw_inicial) + ', Angulo: '+ str(yaw))
            #rospy.loginfo('Yaw anterior :' +str(yaw_anterior) + ' cambio signo :' + str(cambiosigno))
            #rospy.loginfo('Request: '+ str(req.longitud*(pi/180)) + ' diferencia :' + str(abs(yaw+cambiosigno*2*pi-yaw_inicial)))
            if (yaw_anterior-1 > yaw): # He puesto el 1 ya que por tolerancia o lo que sea, a veces si eran iguales se cumplía la condición. Me interesa el signo
                cambiosigno = 1 # Por si pasa de 3.14 a -3.14
            if abs(yaw+cambiosigno*2*pi-yaw_inicial) > req.longitud*(pi/180): # Compruebo que el ángulo actual ha alcanzado al deseado
                command.angular.z = 0 # rad/s
                pub.publish(command)
                terminado = 1
                rospy.loginfo('Angulo inicial: ' + str(yaw_inicial) + ', Angulo final: '+ str(yaw))
                return InitiateMove2Response(1)
            yaw_anterior = yaw 
    else:
        terminado =1
    

def get_position(msg: Odometry):
    global posicionx
    global posiciony
    posicionx = msg.pose.pose.position.x
    posiciony = msg.pose.pose.position.y
    #rospy.loginfo('Posicion: ' + str(posicionx))

def get_rotation(msg: Odometry):
    global roll, pitch, yaw
    orientation_q = msg.pose.pose.orientation
    orientation_list = [orientation_q.x,orientation_q.y, orientation_q.z, orientation_q.w ]
    (roll, pitch, yaw) = euler_from_quaternion(orientation_list)
    #rospy.loginfo('Angle: ' + str(yaw))

def get_obstacle(msg: LaserScan):
    global obstaculo
    obstaculo = msg.ranges[0] # Miro solo obstaculo en frente
    

if __name__ == '__main__':
    command = Twist()
    sub = rospy.Subscriber('/odom', Odometry, get_rotation)
    sub = rospy.Subscriber('/odom', Odometry, get_position)
    sub = rospy.Subscriber('/scan', LaserScan, get_obstacle)
    rospy.init_node('moverseservidor')
    s = rospy.Service('move', InitiateMove2, mueveRobot)
    rospy.loginfo("Ready to move.")
    rospy.spin()