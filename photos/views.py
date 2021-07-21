from django.shortcuts import redirect, render
from .models import Category, Photo
from django.core.paginator import Paginator
from PIL import Image
from django.core.files.base import ContentFile
from io import StringIO

# Create your views here.

def gallery(request):
    category = request.GET.get('category')
    if category == None:
        photos = Paginator(Photo.objects.all(),8)
    else:
        photos = Paginator(Photo.objects.filter(category__name = category), 8)
        
    categories = Category.objects.all()

    
    page = request.GET.get('page')
    imagee = photos.get_page(page)
    
    context = {'categories': categories, 'photos':photos, 'imagee':imagee}
    return render(request, 'photos/gallery.html', context)

def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo':photo})

def addPhoto(request):
    categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        images = request.FILES.getlist('images')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        for image in images:
            photo = Photo.objects.create(
                category = category,
                description = data['description'],
                image = image,
            )

        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)

# def rotateLeft(request,pk):
#     photo = Photo.objects.get(id=pk)
#     Original_Image = Image.open(photo)
#     rotated_image = Original_Image.rotate(90)
#     rotated_image.save('photo',overwrite=True)

#     return render(request, 'photos/rotateLeft.html', {'photo':photo})

# def rotateRight(request,pk):
#     photo = Photo.objects.get(id=pk)
#     Original_Image = Image.open(photo,'r')
#     rotated_image = Original_Image.rotate(180)
#     rotated_image.save('photo',overwrite=True)

#     return render(request, 'photos/rotateRight.html', {'photo':photo})


def rotateLeft(request, pk):
    myModel = Photo.objects.get(id=pk)

    original_photo = StringIO(Photo.file.read())
    rotated_photo = StringIO()

    image = Image.open(original_photo)
    image = image.rotate(-90)
    image.save(rotated_photo, 'JPEG')

    myModel.file.save(image.file.path, ContentFile(rotated_photo.getvalue()))
    myModel.save(overwrite=True)

    return render(request, 'photos/rotateLeft',{'myModel': myModel})
