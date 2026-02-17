from django.contrib.auth import get_user_model
User = get_user_model()

try:
    u = User.objects.get(username='admin')
    print(f"User found: {u.username}")
    print(f"Email: {u.email}")
    print(f"Is Superuser: {u.is_superuser}")
    print(f"Is Staff: {u.is_staff}")
    print(f"Role: {u.role}")  # Checking custom role field
    print(f"Password set: {u.password.startswith('pbkdf2')}")
    
    # Ensure role is admin
    if u.role != 'admin':
        print("Fixing role to 'admin'...")
        u.role = 'admin'
        u.save()
        print("Role updated to 'admin'")
        
except User.DoesNotExist:
    print("User 'admin' NOT found.")
except Exception as e:
    print(f"Error: {e}")
