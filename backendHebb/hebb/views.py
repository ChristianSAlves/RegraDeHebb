from rest_framework.views import APIView
from rest_framework.response import Response
from .models import HebbModel
from .serializers import HebbModelSerializer

class PerceptronTrainView(APIView):
    def post(self, request):
        try:
            # Dados simples para teste
            letra_A = [[-1]*10 for _ in range(10)]
            letra_B = [[-1]*10 for _ in range(10)]

            # Define a estrutura da letra "A"
            for i in range(10):
                if i == 3 or i == 6:
                    letra_A[i][i+1:i+3] = [1, 1]
                elif i >= 4 and i <= 6:
                    letra_A[i][i-1:i+2] = [1, 1, 1]
                elif i == 7:
                    letra_A[i][:10] = [1]*10
                elif i >= 8 and i <= 9:
                    letra_A[i][i-2:i+1] = [1, 1, 1]

            # Define a estrutura da letra "B"
            for i in range(10):
                if i < 2 or i >= 4 and i <= 6 or i == 9:
                    letra_B[i][0:5] = [1]*5
                elif i == 2 or i == 3 or i == 7 or i == 8:
                    letra_B[i][0] = letra_B[i][4] = 1

            matrices = [letra_A, letra_B]  # Matriz de entrada
            y = [1, -1]  # Saídas esperadas
            w = [0] * 100  # Pesos iniciais zerados
            b = 0.0  # Bias inicial zerado
            learning_rate = 0.1  # Taxa de aprendizado

            # Transformando a matriz para ficar mais fácil a análise, praticamente vira um vetor
            def flatten(matrix):
                return [item for sublist in matrix for item in sublist]

            # Aplicação do algoritmo do Perceptron
            for i in range(2):
                flattened_matrix = flatten(matrices[i])
                delta_teste = sum([w[j] * flattened_matrix[j] for j in range(100)]) + b
                prediction = 1 if delta_teste >= 0 else -1

                if prediction != y[i]:  # Atualiza os pesos e bias apenas se houver erro
                    delta_w = [learning_rate * flattened_matrix[j] * y[i] for j in range(100)]
                    delta_b = learning_rate * y[i]
                    w = [w[j] + delta_w[j] for j in range(100)]
                    b += delta_b

            # Salvar pesos e bias diretamente no banco de dados
            model, created = HebbModel.objects.get_or_create(id=1)
            model.weights = w
            model.bias = b
            model.save()

            serializer = HebbModelSerializer(model)
            return Response({"message": "Modelo treinado com sucesso!", "model": serializer.data})

        except Exception as e:
            print("Erro:", e)
            return Response({"error": str(e)}, status=500)

class PerceptronPredictView(APIView):
    def post(self, request):
        matrix = request.data.get("matrix")
        print("Matriz enviada (antes da conversão): ", matrix)

        # Substituir 0 por -1
        matrix = [-1 if x == 0 else x for x in matrix]
        print("Matriz enviada (após a conversão): ", matrix)

        # Recuperar pesos e bias do banco de dados
        try:
            model = HebbModel.objects.get(id=1)
            w = model.weights
            b = model.bias
            print("Pesos recuperados:", w)
            print("Bias recuperado:", b)
        except HebbModel.DoesNotExist:
            return Response({"error": "Modelo não treinado."}, status=400)

        # Verificar se a matriz tem o tamanho correto
        if not isinstance(matrix, list) or len(matrix) != 100:
            return Response({"error": "A matriz deve ter 100 elementos."}, status=400)

        # Aplicar pesos e bias à nova matriz
        delta_teste = sum([w[j] * matrix[j] for j in range(100)]) + b
        print(f"Delta teste calculado: {delta_teste}")
        
        resultado = 1 if delta_teste >= 0 else -1

        # Mapeamento dos resultados para letras
        letras = {1: "A", -1: "B"}
        letra_reconhecida = letras.get(resultado, "Desconhecida")

        return Response({"result": letra_reconhecida})







