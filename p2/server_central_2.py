import grpc
from concurrent import futures
import task_pb2
import task_pb2_grpc

# Implémentation du service du serveur central
class TaskDistributorServicer(task_pb2_grpc.TaskDistributorServicer):
    def DistributeTask(self, request, context):
        # Implémentation de la distribution des tâches aux serveurs clients
        # Ici, vous pouvez implémenter la logique pour sélectionner les clients appropriés et leur envoyer les tâches

        # Pour cet exemple, nous supposons que le message de requête contient uniquement la description de la tâche
        integers = request.integers
        print(integers)
        # TODO: Implémenter la logique de distribution des tâches aux clients
        sum = 0
        # Supposons que les clients aient exécuté les tâches et renvoyé les résultats dans une liste
        for num in integers:
            sum += num

        # Regroupement des résultats dans un message de réponse
        response = task_pb2.TaskResponse(result=sum)
        return response


def run_server():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    task_pb2_grpc.add_TaskDistributorServicer_to_server(TaskDistributorServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    print("Serveur central démarré sur le port 50052...")
    server.wait_for_termination()



if __name__ == '__main__':
    run_server()
