import grpc
import task_pb2
import task_pb2_grpc
import tkinter as tk
import re
def run_client():
    channel = grpc.insecure_channel('localhost:50051')
    stub = task_pb2_grpc.TaskDistributorStub(channel)

    # Supposons que l'utilisateur soumet une tâche via l'interface utilisateur
    task_description = "Tâche à exécuter"

    # Création du message de requête
    request = task_pb2.TaskRequest(description=task_description)

    # Appel de la méthode RPC sur le serveur central
    response = stub.DistributeTask(request)

    # Traitement des résultats reçus du serveur central
    for result in response.results:
        print(result)




def calculate_function(content):
    # regex of integers (positive or negative) separeted by commas
    regex = r"-?\d+(?:,-?\d+)*"
    
    # check if input match regex
    if not re.match(regex, content):
        print("Format invalide")
        raise ValueError("Format invalide")
    
    # convert string to list
    content = content.split(",")
    content = [int(num) for num in content]
    
    # calculate sum of numbers
    channel1 = grpc.insecure_channel('localhost:50051')
    channel2 = grpc.insecure_channel('localhost:50052')
    stub1 = task_pb2_grpc.TaskDistributorStub(channel1)
    stub2 = task_pb2_grpc.TaskDistributorStub(channel2)

    # Création du message de requête
    request1 = task_pb2.TaskRequest(integers=content[:len(content)//2])
    request2 = task_pb2.TaskRequest(integers=content[len(content)//2:])

    # Appel de la méthode RPC sur le serveur central
    result1 = stub1.DistributeTask(request1)
    result2 = stub2.DistributeTask(request2)
    
    result = result1.result + result2.result
    
    result_field.delete(1.0, tk.END)  # Clear previous result
    result_field.insert(tk.END, result)  # Display new result
    result_field.pack(fill=tk.BOTH, padx=10, pady=10)

    print("Result:", result)

def calculate_button_clicked():
    content = entry.get()
    calculate_function(content)

def cancel_button_clicked():
    root.destroy()

root = tk.Tk()
root.title("Text Field Window")

# Set the window size
window_width = 400
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a text field
entry = tk.Entry(root)
entry.pack(fill=tk.BOTH, padx=10, pady=10)

# Create the Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_button_clicked)
calculate_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create the Cancel button
cancel_button = tk.Button(root, text="Cancel", command=cancel_button_clicked)
cancel_button.pack(side=tk.LEFT, padx=10, pady=10)

# Create the result field
result_field = tk.Text(root, height=5)
result_field.pack(fill=tk.BOTH, padx=10, pady=10)

if __name__ == '__main__':
    #run_client()
    root.mainloop()
