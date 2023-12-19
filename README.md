# 🚀 Repositorio de Experimentación: CI/CD y Despliegue en AWS App Runner

<p align="center">
  <img src="img/1.png" alt="AppRunner" width="150">
  <img src="img/2.png" alt="Actions" width="150">
</p>




## ¡Bienvenido a la Central de Innovación! 👋

¡Saludos, explorador del código! Aquí en mi laboratorio digital, estamos inmersos en una emocionante aventura de desarrollo, donde las ideas toman vida y la experimentación es la norma. Este repositorio es el epicentro de nuestras hazañas, donde exploramos los encantos de GitHub Actions, CI/CD, y llevamos nuestras creaciones a nuevas alturas con AWS App Runner.

## 🧪 Experimentos en Acción

### Flujos de CI/CD con GitHub Actions

Profundiza en los entresijos de nuestros flujos de CI/CD explorando los archivos YAML en `/.github/workflows`. Cada archivo cuenta la historia de pruebas automatizadas, despliegues en AWS y más.

## 🛠️ Tecnologías Estelares

- **Interfaz de Usuario:**
  - HTML, JavaScript y CSS para una experiencia cautivadora.
- **Funcionalidades Avanzadas:**
  - Python con librerías como Three.js para llevar nuestras creaciones al siguiente nivel.
- **Automatización con GitHub Actions:**
  - Flujos personalizados para CI/CD que simplifican nuestro camino.
- **Empaque y Envío:**
  - Docker, nuestro aliado para empaquetar y enviar aplicaciones sin complicaciones.
- **Despliegue Eficiente:**
  - AWS App Runner para despliegues ágiles y escalables.

## 🌐 Instrucciones de Implementación

1. **Configuración del Entorno AWS:**
   - Crea tu cuenta en AWS.
   - Configura tus credenciales y sintoniza AWS App Runner desde la consola.


2. **Personaliza y Desata tu Creatividad:**
   - Modifica el contenido HTML, perfecciona funciones JavaScript o añade tu toque único. ¡Hazlo tuyo!

3. **A partir de aca comienza la implementacion**

```YML
# Example
name: Deploy to App Runner 
on:
  push:
    branches: [ main ] 
  workflow_dispatch:
jobs:  
  deploy:
    runs-on: ubuntu-latest
    
    steps:      
      - name: Checkout
        uses: actions/checkout@v2
        with:
          persist-credentials: false
          
      - name: Configure AWS credentials
        id: aws-credentials
        uses: aws-actions/configure-aws-credentials@v1
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: ${{ secrets.AWS_REGION }}     

      - name: Login to Amazon ECR
        id: login-ecr
        uses: aws-actions/amazon-ecr-login@v1        

      - name: Build, tag, and push image to Amazon ECR
        id: build-image
        env:
          ECR_REGISTRY: ${{ steps.login-ecr.outputs.registry }}
          ECR_REPOSITORY: app-google
          IMAGE_TAG: ${{ github.sha }}
        run: |
          docker build -t $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG .
          docker push $ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG
          echo "::set-output name=image::$ECR_REGISTRY/$ECR_REPOSITORY:$IMAGE_TAG"  
          
      - name: Deploy to App Runner
        id: deploy-apprunner
        uses: awslabs/amazon-app-runner-deploy@main        
        with:
          service: app-runner-service
          image: ${{ steps.build-image.outputs.image }}          
          access-role-arn: ${{ secrets.ROLE_ARN }}
          runtime: PYTHON_3          
          region: ${{ secrets.AWS_REGION }}
          cpu : 1
          memory : 2
          port: 8080
          wait-for-service-stability-seconds: 300
      
      - name: App Runner output
        run: echo "App runner output ${{ steps.deploy-apprunner.outputs.url }}"
```

## 🚀 ¡Tu Aventura Comienza Ahora!

Embárcate en tu propia odisea de experimentación y despliegue continuo. Abre issues, crea pull requests y comparte tus ideas. Este repositorio es un espacio para la colaboración y el aprendizaje conjunto.

¡Que disfrutes explorando y creando! 🌟 Happy coding! 🚀✨


```
