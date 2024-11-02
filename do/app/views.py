from django.shortcuts import render,redirect,get_object_or_404

from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.auth.models import User

from .models import Task

# Create your views here.
def logout_view(request):
    logout(request)
    messages.success(request, 'Vous êtes maintenant déconnecté.')
    return redirect('login')


def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        # Vérifiez si les mots de passe correspondent
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
            return render(request, 'sign_up.html')

        # Vérifiez si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur est déjà pris.")
            return render(request, 'sign_up.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Cette adresse e-mail est déjà utilisée.")
            return render(request, 'sign_up.html')

        # Créez l'utilisateur
        user = User.objects.create_user(username=username, email=email, password=password1)
        user.save()
        messages.success(request, f'Compte créé avec succès pour {username} ! Vous pouvez maintenant vous connecter.')
        return redirect('login')  # Redirige vers la page de connexion

    return render(request, 'sign_up.html')  # Affiche le formulaire d'inscription


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirigez vers votre page d'accueil ou un tableau de bord
        else:
            messages.error(request, 'Nom d’utilisateur ou mot de passe incorrect.')
    return render(request, 'login.html',{'messages':messages})


def index(request):
    # Vérifiez si l'utilisateur est authentifié
    if request.user.is_authenticated:
        tache = Task.objects.filter(user=request.user)
        print(tache)
    else:
        tache = Task.objects.none()  # Si l'utilisateur n'est pas connecté, aucune tâche n'est retournée
    
    return render(request, 'index.html', {'taches': tache})


def ajouter(request):
    # Vérifiez si l'utilisateur est authentifié avant tout
    if not request.user.is_authenticated:
        messages.error(request, "Vous devez être connecté pour ajouter une tâche.")
        return redirect('login')  # Rediriger vers la page de connexion si non authentifié

    if request.method == 'POST':
        taches = request.POST.get('taches')
        date= request.POST.get('date')
        if taches:  # Vérifiez si une tâche a été soumise
            try:
                # Créer une nouvelle tâche
                nouvelle_tache = Task(name=taches,date=date, user=request.user)  # Utilisez le bon champ selon votre modèle
                nouvelle_tache.save()
                messages.success(request, "Tâche ajoutée avec succès!")  # Message de succès
                return redirect('index')  # Rediriger vers l'index après l'ajout
            except Exception as e:
                print(f"Erreur lors de l'ajout de la tâche: {e}")  # Imprime l'erreur pour le débogage
                messages.error(request, "Une erreur s'est produite lors de l'ajout de la tâche.")  # Message d'erreur
        else:
            messages.warning(request, "Veuillez entrer une tâche.")  # Message d'avertissement si aucune tâche n'est entrée

    return redirect('index')



def toggle_task(request, task_id):
    try:

        task = get_object_or_404(Task, id=task_id, user=request.user)  # Récupérer la tâche par ID
        task.completed = not task.completed  # Inverser l'état de completed
        task.save()  # Sauvegarder les modifications
        return redirect('index')  # Rediriger vers l'index
    except :
        print("err")