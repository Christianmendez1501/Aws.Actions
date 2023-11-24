# ¡Bienvenido a mi Repositorio de GitHub! 🚀

¡Hola, viajero del código! Este rincón de GitHub es mi patio de juegos para experimentar con Git, GitHub Actions, CI/CD, y más.

## Acerca de este Repositorio

Este repositorio es mi laboratorio personal, donde realizamos emocionantes experimentos con GitHub Actions para desplegar una página web de tipo formulario. Fusionamos las potentes herramientas de HTML, JavaScript, y CSS, junto con la ejecución magistral de Python y sus bibliotecas, como Three.js, para crear una experiencia única.

Implementamos un fluido flujo de integración continua/despliegue continuo (CI/CD) utilizando diversos agentes, entre ellos, GitHub Actions, para automatizar todo el proceso. No solo eso, también nos sumergimos en el mundo de Docker y un registro de contenedores, construyendo y enviando imágenes con maestría. Para coronar nuestra hazaña, utilizamos App Runner para desplegar la página web de manera eficiente y sin complicaciones.

La implementacion continua comienza en Github.Actions a partir de una archivo YML:

```YML
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

## ¡Diviértete Explorando!

Si tienes alguna idea, sugerencia o simplemente quieres compartir tus propios experimentos, ¡no dudes en abrir issues o pull requests! Este repositorio es un espacio abierto para la colaboración y el aprendizaje conjunto.

¡Espero que disfrutes tu visita y encuentres algo interesante para llevarte! 🌟

Happy coding! 🚀✨
