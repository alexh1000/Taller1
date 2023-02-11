# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 22:36:28 2023

@author: Nicolás Rincón Sánchez - 202021963
"""

import pynput
from pynput.keyboard import Key, Listener

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Twist

class TurtleBotTeleop(Node):

    def __init__(self):
	# Inicializar la superclase Nodo de la cual hereda con el nombre requerido
        super().__init__('turtle_bot_teleop')
        # Asignar a los atributos de velocidad los parámetros ingresados
        self.linear = float(input("Por favor ingrese la velocidad lineal (en cm/s - max70): "))
        self.angular = float(input("Por favor ingrese la velocidad angular (en deg/s - max180): "))
        # Publicar en el tópico turtlebot_cmdVel el mensaje tipo Twist
        self.publisher_ = self.create_publisher(Twist,'turtlebot_cmdVel', 10)
        # Definir el Listener de la librería pynput para que detecte tecleo
        with Listener(on_press=self.callback_pressed, on_release=self.callback_released) as listener:
            listener.join()
        # Inicializar el Listener dentro del constructor de la clase
        listener.start()


    # =============== FUNCIONES DE LA LIBRERÍA ===============
    def callback_pressed(self, key):
        # Actualización de velocidades cuando se oprime una tecla
        vel_msg = Twist()
        # Primer movimiento del robot - Traslacional hacia adelante
        if key == Key.up:
            vel_msg.linear.x = self.linear
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = 0.0
            self.get_logger().info('Movimiento traslacional hacia Adelante') 
        # Segundo movimiento del robot - Traslacional hacia atrás
        elif key == Key.down:
            vel_msg.linear.x = -1*self.linear
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = 0.0
            self.get_logger().info('Movimiento traslacional hacia Atrás')
        # Tercer movimiento del robot - Rotacional hacia la derecha (clockwise)
        elif key == Key.right:
            vel_msg.linear.x = 0.0
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = -1*self.angular
            self.get_logger().info('Movimiento rotacional hacia la Derecha')
        # Cuarto movimiento del robot - Rotacional hacia la izquierda (counterclockwise)
        elif key == Key.left:
            vel_msg.linear.x = 0.0
            vel_msg.linear.y = 0.0
            vel_msg.linear.z = 0.0
            vel_msg.angular.x = 0.0
            vel_msg.angular.y = 0.0
            vel_msg.angular.z = self.angular
            self.get_logger().info('Movimiento rotacional hacia la Izquierda')
        # Realizar la publicación de los datos actualizados de velocidad
        self.publisher_.publish(vel_msg)
        

    def callback_released(self, key):
        # Actualización a cero de las velocidades cuando se suelta una tecla
        vel_msg = Twist()
        vel_msg.linear.x = 0.0
        vel_msg.linear.y = 0.0
        vel_msg.linear.z = 0.0
        vel_msg.angular.x = 0.0
        vel_msg.angular.y = 0.0
        vel_msg.angular.z = 0.0
        self.publisher_.publish(vel_msg)
        self.get_logger().info('No hay teclas presionadas. El robot se está deteniendo.')
        if key == Key.esc:
            # Stop listener when ESC is pressed
            return False   
        

# =============== MÉTODO MAIN PARA EJECUCIÓN ===============
def main(args=None):
    rclpy.init(args=args)

    turtle_bot_teleop = TurtleBotTeleop()

    rclpy.spin(turtle_bot_teleop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    turtle_bot_teleop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
