# System Design
Se propone un diseño de sistema serverless basado en AWS. Aunque no es estrictamente necesario implementar todos los módulos descritos inicialmente, se recomienda comenzar con la implementación de **AWS API Gateway**, **AWS Lambda** y **DynamoDB**, ya que estos componentes son paralelos al proyecto actual y cumplen con los requisitos clave del sistema.

**Fuente**:
https://docs.aws.amazon.com/es_es/whitepapers/latest/serverless-multi-tier-architectures-api-gateway-lambda/microservices-with-lambda.html

## **1. Arquitectura General**

### **Componentes principales**

1. **Frontend para los Clientes (Opcional)**:
   - Una aplicación web o dashboard donde los clientes puedan consultar datos procesados o interactuar con el sistema.
   - Implementado con servicios como AWS Amplify para reducir costos.

2. **API Gateway**:
   - Recibe las solicitudes de las aplicaciones cliente.
   - Configura **Rate Limiting** usando AWS API Gateway.
   - Aplica políticas de seguridad mediante **API Keys** o **AWS Cognito** para autenticar a los clientes.

3. **Lambda Functions**:
   - Implementa la lógica principal para procesar eventos.
   - Divide la lógica de los tres microservicios actuales (**Events**, **Stories** y **Tests**) en funciones Lambda separadas.
   - Incluye validaciones, transformación de datos y coordinación con otros servicios como DynamoDB y S3, si se requiere.

4. **Base de Datos**:
   - **DynamoDB**:
     - Almacena los eventos procesados.
     - Diseñada para soportar la alta concurrencia con capacidad provisionada escalable.
     - Tablas separadas para cada tipo de datos (eventos, historias, tests).
   - **Amazon S3**:
     - Almacenamiento de logs y backups.

5. **Cola de Mensajes**:
   - **Amazon SQS**:
     - Implementa comunicación asincrónica para desacoplar los componentes del sistema.
     - Asegura que los eventos se procesen ordenados y sin perdidas.

6. **Monitoreo y Logs**:
   - **AWS CloudWatch**:
     - Monitorea métricas clave.
     - Almacena logs de las Lambda Functions y del API Gateway para auditoría.

---

## **2. Seguridad**

1. **Autenticación y Autorización**:
   - Uso de **API Keys** o integración con **AWS Cognito**.
   - Permite gestionar los clientes registrados y asignar permisos, para poder gestionar trabajos en un equipo de desarrolladores.

2. **Rate Limiting**:
   - Configuración de límites de solicitudes por segundo en API Gateway para prevenir abuso.
   - Alertas configuradas en CloudWatch para detectar picos de tráfico sospechoso.

3. **Protección contra ataques DDoS**:
   - **AWS Shield Basic**: Proporciona protección gratuita contra ataques DDoS básicos.
   - **WAF (Web Application Firewall)**: Aplica reglas para bloquear patrones de ataque conocidos.

---

## **3. Escalabilidad**

- **AWS Lambda**:
  - Escala automáticamente según el número de solicitudes, manejando hasta 2k aplicaciones enviando eventos.
- **DynamoDB**:
  - Provisión de capacidad para leer/escribir datos según la carga esperada.
  - Uso de índices secundarios para mejorar el rendimiento en consultas específicas.
- **S3**:
  - Escala automáticamente para almacenar datos históricos o grandes volúmenes de logs.

---

---

## **4. Gestión del Sistema**

- **Simplificación para el equipo**:
  - Uso de servicios serverless (Lambda, DynamoDB, S3) reduce la complejidad de mantenimiento.
  - Despliegue automatizado con herramientas de IaC (Terraform).
  - Monitoreo centralizado con AWS CloudWatch.

---

## **5. Áreas de Mejora a Futuro**

1. **Integración de Machine Learning**:
   - Uso de AWS SageMaker para identificar patrones avanzados en los eventos o historias.

2. **Soporte para Big Data**:
   - Almacenar datos históricos en Amazon Redshift para análisis avanzado.

3. **Escalabilidad Avanzada**:
   - Migrar a contenedores (ECS o EKS) si la carga supera las capacidades actuales.


