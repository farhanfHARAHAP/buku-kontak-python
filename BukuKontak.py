import webbrowser
from tabulate import tabulate
import os

class BukuKontak:

    def __init__(self):
        dataDir = 'data.txt'
        self.contactData = []
        with open(dataDir, 'r') as file:
            data = file.read().split('\n')
            if data:
                for contact in data:
                    contact = contact.split('$')
                    self.contactData.append({
                        'name' : contact[0],
                        'whatsapp' : contact[1],
                        'relation' : contact[2]
                    })


    def createContact(self, name:str, whatsapp:str, relation:str):
        # name, whatsapp, and relation cant contain$
        if not('$' in name or '$' in relation or whatsapp in [str(x['whatsapp']) for x in self.contactData]) :
            self.contactData.append({
                'name': name,
                'whatsapp': whatsapp,
                'relation': relation
            })
            return True
        else:
            return False

    def findContactByNumber(self, whatsapp:str):
        result = []
        for contact in self.contactData:
            if contact['whatsapp'] == whatsapp:
                result.append(contact)
        return result
    
    def findContactByName(self, name:str):
        result = []
        for contact in self.contactData:
            if name in contact['name']:
                result.append(contact)
        return result
    
    def deleteContact(self, contacts:list):        
        for contact in contacts:
            self.contactData.remove(contact)
    
    def chatWhatsapp(self, contacts:list):
        if contacts != []:
            for contact in contacts:
                webbrowser.open_new_tab(f'https://wa.me/{contact['whatsapp']}')

    def save(self):
        newData = []
        for contact in self.contactData:
            newData.append('$'.join([contact['name'], contact['whatsapp'], contact['relation']]))
        newData = '\n'.join(newData)
            
        with open('data.txt', 'w') as file:
            file.write(newData)        

    def makeTable(self, contacts:list):
        contacts = [list(contact.values()) for contact in contacts]
        print('\n')
        print(tabulate(contacts, headers=['Nama', 'Whatsapp', 'Relasi']))

def clear():
    os.system('cls')

def main():
    # / credit
    print('''
// Farhan Fadillah Harahap
/// Maxy Academy 2024
//// Backend Student 
///// Universitas Trisakti
            
$$ BUKU KONTAK PYTHON $$              
                                                                                
            ''')
    
    input('PRESS ENTER TO START')
    clear()
    
    bukuKontak = BukuKontak()
    showPage = '/home'

    while True:
    
        # /home
        while showPage == '/home':
            clear()
            print('''
$ Menu Awal (/home) $
1. Lihat Kontak
2. Tambah Kontak
3. Hapus Kontak
4. Edit Kontak
                                                                                            
                    ''')
            
            userInput = str(input('>> '))

            if(userInput == '1'):
                showPage = '/show'
            elif(userInput == '2'):
                showPage = '/insert'
            elif(userInput == '3'):
                showPage = '/delete'
            elif(userInput == '4'):
                showPage = '/edit'
            else:
                print(f'! No option {userInput} in this page !\n')
                input('ENTER TO CONTINUE')            
        
        # /show
        while showPage == '/show':
            clear()
            print('''
$ Menu Lihat Kontak (/show) $
1. SEMUA
2. berdasarkan NAMA (otomatis membuka WA)                                   
3. berdasarkan WHATSAPP (otomatis membuka WA)            
0. << Kembali                          
                    
                    ''')
            
            userInput = str(input('>> '))

            selectedContact = []
            if(userInput == '1'):
                selectedContact = bukuKontak.contactData                
                bukuKontak.makeTable(selectedContact)
                input('ENTER TO CONTINUE')                            
            elif(userInput == '2'):
                selectedContact = bukuKontak.findContactByName(str(input('NAMA >> ')))
                bukuKontak.makeTable(selectedContact)
                input('ENTER TO CONTINUE') 
                bukuKontak.chatWhatsapp(selectedContact)    
            elif(userInput == '3'):
                selectedContact = bukuKontak.findContactByNumber(str(input('WHATSAPP >> ')))
                bukuKontak.makeTable(selectedContact)
                input('ENTER TO CONTINUE') 
                bukuKontak.chatWhatsapp(selectedContact)    
            elif(userInput == '0'):
                showPage = '/home'
            else:
                print(f'! No option {userInput} in this page !\n')
                input('ENTER TO CONTINUE')    

        # /insert
        while showPage == '/insert':
            clear()
            print('''
$ Tambah Kontak (/insert) $

[ATURAN]
+ Nama dan Relasi tidak boleh mengandung karakter $.                
+ Mulailah nomor Whatsapp dengan nomor negara (Indonesia 62).        
+ Nomor whatsapp tidak boleh sama dengan kontak yang tersimpan.                                                 
                    
                    ''')
            
            nama = str(input('NAMA >> '))
            whatsapp = str(input('WHATSAPP >> '))
            relasi = str(input('RELASI >> '))

            if (bukuKontak.createContact(nama, whatsapp, relasi)):
                print(f'''

NAMA: {nama}
WHATSAPP: {whatsapp}
RELASI: {relasi}

Konfirmasi untuk menyimpan (y/n) default y
                      ''')
                userInput = input('KONFIRMASI >> ')
                if(userInput == '' or userInput == 'y'):
                    bukuKontak.save()
                    print('! Perubahan disimpan. !')
                    input('ENTER TO CONTINUE')
                else:
                    bukuKontak.deleteContact(bukuKontak.findContactByNumber(whatsapp))
                    print('! Perubahan ditangguhkan. !')
                    input('ENTER TO CONTINUE')
            else:
                print('! Input anda menyalahi aturan. !')
                input('ENTER TO CONTINUE')

            showPage = '/home'

        # /delete    
        while showPage == '/delete':
            clear()
            print('''
$ Hapus Kontak (/delete) $

1. berdasarkan NAMA (bisa banyak sekaligus)                                   
2. berdasarkan NOMOR WHATSAPP   
0. << Kembali                                 
                    
                    ''')
            userInput = str(input('>> '))
            if(userInput == '1'):
                showPage = '/delete/byName'
            elif(userInput == '2'):
                showPage = '/delete/byWA'
            elif(userInput == '0'):
                showPage = '/home'
            else:
                print(f'! No option {userInput} in this page !\n')
                input('ENTER TO CONTINUE') 

        # /delete/byName
        while showPage == '/delete/byName':
            clear()
            print('''
$ Hapus Kontak (/delete/byName) $

[NOTES] 
+ Jika ada kesamaan nama, maka kontak akan dihapus juga.                                              
                    
                    ''')
            
            nama = str(input('NAMA >> '))
            selectedContact = bukuKontak.findContactByName(nama)
            if(selectedContact != []):
                bukuKontak.makeTable(selectedContact)
                print('''
Konfirmasi untuk menghapus kontak di tabel (y/n) default y  
                                          
                      ''')
                userInput = input('>> ')
                if(userInput == 'y' or userInput == ''):
                    bukuKontak.deleteContact(selectedContact)
                    bukuKontak.save()
                    print('! Perubahan disimpan. !')
                    input('ENTER TO CONTINUE')
                else:
                    print('! Perubahan ditangguhkan. !')
                    input('ENTER TO CONTINUE')
            else:
                print(f'! Tidak ditemukan kontak bernama {nama}. !')
                input('ENTER TO CONTINUE')
            showPage = '/delete'

        # /delete/byWA
        while showPage == '/delete/byWA':
            clear()
            print('''
$ Hapus Kontak (/delete/byWA) $                                         
                    
                    ''')
            
            whatsapp = str(input('WHATSAPP >> '))
            selectedContact = bukuKontak.findContactByNumber(whatsapp)
            if(selectedContact != []):
                bukuKontak.makeTable(selectedContact)
                print('''
Konfirmasi untuk menghapus kontak di tabel (y/n) default y  
                                          
                      ''')
                userInput = input('>> ')
                if(userInput == 'y' or userInput == ''):
                    bukuKontak.deleteContact(selectedContact)
                    bukuKontak.save()
                    print('! Perubahan disimpan. !')
                    input('ENTER TO CONTINUE')
                else:
                    print('! Perubahan ditangguhkan. !')
                    input('ENTER TO CONTINUE')
            else:
                print(f'! Tidak ditemukan kontak bernomor WA {whatsapp}. !')
                input('ENTER TO CONTINUE')
            showPage = '/delete'

        # /edit
        while showPage == '/edit':
            clear()
            print('''
$ Edit Kontak (/edit) $                                         

[NOTES]                                      
+ Yang dapat diedit hanyalah nama dan relasi, hapus kontak jika anda ingin mengubah no. WA 
                                   
                    ''')
            
            whatsapp = str(input('WHATSAPP >> '))
            selectedContact = bukuKontak.findContactByNumber(whatsapp)            
            if(selectedContact != []):                
                bukuKontak.makeTable(selectedContact)
                print('\n')
                nama = str(input('NAMA (BARU) >> '))
                relasi = str(input('RELASI (BARU) >> '))
                print('''
Konfirmasi untuk mengedit kontak di tabel (y/n) default y  
                                          
                      ''')
                userInput = input('>> ')
                if(userInput == 'y' or userInput == ''):
                    bukuKontak.deleteContact(selectedContact)
                    bukuKontak.createContact(nama, whatsapp, relasi)
                    bukuKontak.save()
                    print('! Perubahan disimpan. !')
                    input('ENTER TO CONTINUE')
                else:
                    print('! Perubahan ditangguhkan. !')
                    input('ENTER TO CONTINUE')
            else:
                print(f'! Tidak ditemukan kontak bernomor WA {whatsapp}. !')
                input('ENTER TO CONTINUE')
            showPage = '/home'        



main()