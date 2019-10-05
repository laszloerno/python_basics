import string
email ="laszlo.erno@gmail.com"
print("Köszönjük regisztrációját!")
felhasz = email[0:email.index("@"):]
doma = email[email.index("@")+1::][:email.index(".")-1]
print("Felhasználónév: {}"+felhasz)
print("Domain: {}"+doma)