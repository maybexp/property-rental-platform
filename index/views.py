import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from branca.element import Figure
from django.urls import reverse

from index.models import *
from django.utils.timesince import timesince
from datetime import datetime

def index(request):
    return render(request, 'index/index.html')

def privacyPolicy(request):
    return render(request, 'index/privacyPolicy.html')

def contact(request):
    return render(request, 'index/about.html')

def about(request):
    return render(request, 'index/about.html')

def signup(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'registration/signup.html')

def search(request, cityName=""):
    if request.POST:
        if request.POST['cityName']:
            cityName = request.POST['cityName']

    cityName = cityName.replace("ae", "æ").replace("oe", "ø").replace("-", " ").title()

    apartments = RentalApartment.objects.filter(address__icontains=cityName)
    if not apartments.exists():
        return render(request, 'index/search.html', {'cityName': cityName})

    city = apartments.first().address.split(",")[-1].strip()
    city = city.translate(str.maketrans('', '', '0123456789')).strip()
    apartmentCount = apartments.count()


    paginator = Paginator(apartments, 21)

    page_number = request.GET.get('side', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'index/search.html',
                  {'cityName': city.replace(".", "").strip(), 'apartments': page_obj, 'apartmentCount': apartmentCount})



import folium
from geopy.geocoders import Nominatim

def rentalApartment(request, rentalApartmentId):
    rentalApartment = RentalApartment.objects.get(id=rentalApartmentId)
    isSaved = None
    isReported = None
    if(request.user.is_authenticated):
        isSaved = SavedApartment.objects.filter(rentalApartment=rentalApartment, user=request.user).exists()
        isReported = ReportRentalApartment.objects.filter(rentalApartment=rentalApartment, user=request.user).exists()


    geolocator = Nominatim(user_agent="boligerne")
    address = rentalApartment.address

    if address.count(',') == 2:
        address_parts = address.split(',')
        address_parts.pop(1)
        address = ', '.join(address_parts)


    location = geolocator.geocode(address)
    try:
        latitude = location.latitude
        longitude = location.longitude
    except:
        latitude = 56.153338
        longitude = 10.171202
    coords = [latitude, longitude]

    fig = Figure(height=200)
    m = folium.Map(location=coords, zoom_start=18, scrollWheelZoom=False)
    fig.add_child(m)

    folium.Circle(location=coords, radius=10, color='red', fill=True, fill_color='red', fill_opacity=0.2).add_to(m)
    city = rentalApartment.address.split(",")[-1].strip()
    city = city.translate(str.maketrans('', '', '0123456789')).strip()
    folium.Marker(location=coords, popup=city).add_to(m)

    html_map = m._repr_html_()

    images = ApartmentImage.objects.filter(rental_apartment=rentalApartment)
    return render(request, 'index/housing.html', {'rentalApartment': rentalApartment, 'images':images, 'html_map': html_map, 'isSaved': isSaved, 'isReported': isReported})

def customerService(request):
    return render(request, 'index/kundeservice.html')

def createHousingPost(request):
    return render(request, 'index/opret-bolig-annonce.html')

@login_required
def myAccount(request):
    apartments = SavedApartment.objects.filter(user=request.user).order_by('-timestamp')
    createdApartments = RentalApartment.objects.filter(user=request.user).order_by('-timestamp')
    return render(request, 'registration/min-konto.html', {'apartments': apartments, 'createdApartments': createdApartments})

def loggedOut(request):
    return render(request, 'registration/logged-out.html')

@login_required
def boligOpsat(request):
    return render(request, 'index/bolig-opsat.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            # Authentication failed
            return redirect('login')
    else:
        return redirect('login')

def tipsTilEnSikkerBolighandel(request):
    return render(request, 'index/tips-til-en-sikker-bolighandel.html')

def anmeldSnyd(request):
    return render(request, 'index/anmeld-snyd.html')

def vilkaar(request):
    return render(request, 'index/vilkaar.html')

def opdateringer(request):
    return render(request, 'index/opdateringer.html')

#Only POST or GET requeists

@login_required
def updateUserInfo(request):
    if request.method == 'POST':
        if request.POST['firstName'] or request.POST['lastName']:
            user = request.user
            if request.POST['firstName'] != '':
                user.first_name = request.POST['firstName'].title()

            if request.POST['lastName'] != '':
                user.last_name = request.POST['lastName'].title()

            user.save()

            redirect_url = reverse('myAccount')

            redirect_url += '#userInfo'
            messages.success(request, 'Dine oplysninger er blevet opdateret.')
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, 'Der opstod en fejl. Prøv igen senere.')
            return redirect("myAccount")

    messages.error(request, 'Fejl - kontakt support: support@boligerne.dk hvis problemet fortsætter')
    return redirect('myAccount')


@login_required
def addApartment(request):
    if request.method == 'POST':
        if request.POST['address'] and request.POST['apartmentType'] and request.POST['squareMeterInput'] and request.POST['housingRooms'] and request.POST['monthlyRent'] and request.POST['deposit'] and request.POST['prepaidRent'] and request.POST['animalsAllowed'] and request.POST['heading'] and request.POST['description'] and request.FILES['img']:
            address = request.POST.get('address')
            apartmentType = request.POST.get('apartmentType')
            squareMeterInput = request.POST.get('squareMeterInput')
            housingRooms = request.POST.get('housingRooms')
            monthlyRent = request.POST.get('monthlyRent')
            deposit = request.POST.get('deposit')
            prepaidRent = request.POST.get('prepaidRent')
            animalsAllowed = request.POST.get('animalsAllowed')

            ## altan, have, elevator, møbleret, parkering

            heading = request.POST.get('heading')
            description = request.POST.get('description')

            email = request.POST.get('email')


            from datetime import datetime

            try:
                apartmentTypeInstance = ApartmentType.objects.get(name=apartmentType)
            except ApartmentType.DoesNotExist:
                print("ApartmentType does not exist")

            try:
                if(animalsAllowed == "allowed"):
                    animalsAllowedNewVar = "Tilladt"
                elif(animalsAllowed == "notAllowed"):
                    animalsAllowedNewVar = "Ikke tilladt"
                elif(animalsAllowed == "contactOwner"):
                    animalsAllowedNewVar = "Kontakt ejer"
                animalsAllowedInstance = AnimalsAllowed.objects.get(status=animalsAllowedNewVar)
            except AnimalsAllowed.DoesNotExist:
                return HttpResponse(animalsAllowed)
                print("Animals allowed type does not exist")

            rental_apartment = RentalApartment.objects.create(
                user=request.user,
                address=address,
                type=apartmentTypeInstance,
                size=squareMeterInput,
                rooms=housingRooms,
                monthlyRent=monthlyRent,
                securityDeposit=deposit,
                prepaidRent=prepaidRent,
                animalsAllowed=animalsAllowedInstance,

                title=heading,
                description=description,
                email=email,
                floor=1
            )
            if request.POST.get('balcony'):
                rental_apartment.balcony = True

            if request.POST.get('garden'):
                garden = request.POST.get('garden')
                rental_apartment.garden = True

            if request.POST.get('elevator'):
                elevator = request.POST.get('elevator')
                rental_apartment.elevator = True

            if request.POST.get('furnished'):
                furnished = request.POST.get('furnished')
                rental_apartment.furnished = True

            if request.POST.get('parking'):
                parking = request.POST.get('parking')
                rental_apartment.parking = True

            if request.POST.get('availableFrom'):
                availableFrom = request.POST.get('availableFrom')
                rental_apartment.availableFrom = datetime.strptime(availableFrom, '%Y-%m-%d').date()

            if request.POST.get('phoneNumber'):
                phoneNumber = request.POST.get('phoneNumber')
                rental_apartment.phoneNumber = phoneNumber

            images = request.FILES.getlist('img')
            for image in images:
                ApartmentImage.objects.create(rental_apartment=rental_apartment, images=image)

            rental_apartment.save()

            return redirect('rentalApartment', rental_apartment.id)
            #return HttpResponse(str(address) + str(apartmentType) + str(squareMeterInput) + str(housingRooms) + str(monthlyRent) + str(deposit) + str(prepaidRent) + str(animalsAllowed) + str(heading) + str(description) + str(images))
        return HttpResponse("no")
            #messages.success(request, 'Dine oplysninger er blevet opdateret.')
            #return redirect('myAccount')
        #else:
            #return redirect("myAccount")

    #messages.error(request, 'Fejl - kontakt support:')


def createUser(request):
    if request.method == 'POST':
        try:
            acceptTermsOfUse = request.POST['acceptTermsOfUse']
        except:
            messages.error(request, "Accepter Boligerne.dk's vilkår i bunden af siden")
            return redirect('signup')

        try:
            password = request.POST['password']
            email = request.POST['email']

            full_name = request.POST['full_name']
            name_parts = full_name.split()
            first_name = name_parts[0].title()
            last_name_parts = name_parts[1:]
            last_name = ' '.join(last_name_parts).title()

            user = User.objects.create_user(email, email, password)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
        except:
            messages.error(request, 'Emailen er allerede i brug.')
            return redirect('signup')

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)

            return redirect('index')
        else:
            messages.error(request, 'Fejl - kontakt support@boligerne.dk hvis problemet ikke stopper')
            return redirect('signup')
    else:
        return render(request, 'create_user.html')

def test(request, cityName):
    cityName = cityName.replace("ae", "æ").replace("oe", "ø").replace("aa", "å").replace("-", " ").title()

    apartments = RentalApartment.objects.filter(address__icontains=cityName).order_by('-timestamp')
    if not apartments.exists():
        return render(request, 'index/search.html', {'cityName': cityName})
    city = apartments.first().address.split(",")[-1].strip()
    city = city.translate(str.maketrans('', '', '0123456789')).strip()
    apartmentCount = apartments.count()

    paginator = Paginator(apartments, 21)

    page_number = request.GET.get('side', 1)
    page_obj = paginator.get_page(page_number)
    return render(request, 'index/test.html',
                  {'cityName': city, 'apartments': page_obj, 'apartmentCount': apartmentCount})

## AJAX

def ajax_view(request):
    # Process the AJAX request
    address = request.GET.get('address')
    maxMonthlyRent = request.GET.get('max_monthly_rent')
    minimumSize = request.GET.get('minimumSize')
    rooms = request.GET.get('rooms')

    checkboxApartment = request.GET.get('checkboxApartment')
    checkboxRoom = request.GET.get('checkboxRoom')
    checkboxHouse = request.GET.get('checkboxHouse')
    checkboxTerracedHouse = request.GET.get('checkboxTerracedHouse')

    balcony = request.GET.get('balcony')
    animalsAllowed = request.GET.get('animalsAllowed')
    elevator = request.GET.get('elevator')
    furnished = request.GET.get('furnished')
    parking = request.GET.get('parking')

    sortMethod = request.GET.get('sortMethod')

    if sortMethod == 'newestFirst':
        sortMethod = '-timestamp'
    if sortMethod == 'cheapestFirst':
        sortMethod = 'monthlyRent'
    if sortMethod == 'expensiveFirst':
        sortMethod = '-monthlyRent'
    if sortMethod == 'smallestFirst':
        sortMethod = 'size'
    if sortMethod == 'biggestFirst':
        sortMethod = '-size'


    # Construct the filter parameters
    filter_params = {'address__contains': address}

    if checkboxApartment == 'true':
        getApartmentType = ApartmentType.objects.get(name='Lejlighed')
        filter_params['type__in'] = [getApartmentType]

    if checkboxRoom == 'true':
        getRoomType = ApartmentType.objects.get(name='Værelse')
        if 'type__in' in filter_params:
            filter_params['type__in'].append(getRoomType)
        else:
            filter_params['type__in'] = [getRoomType]

    if checkboxHouse == 'true':
        getHouseType = ApartmentType.objects.get(name='Hus')
        if 'type__in' in filter_params:
            filter_params['type__in'].append(getHouseType)
        else:
            filter_params['type__in'] = [getHouseType]

    if checkboxTerracedHouse == 'true':
        getTerracedHouseType = ApartmentType.objects.get(name='Rækkehus')
        if 'type__in' in filter_params:
            filter_params['type__in'].append(getTerracedHouseType)
        else:
            filter_params['type__in'] = [getTerracedHouseType]

    if maxMonthlyRent:
        filter_params['monthlyRent__lte'] = maxMonthlyRent
    if minimumSize:
        filter_params['size__gte'] = minimumSize
    if rooms:
        filter_params['rooms__gte'] = rooms

    if balcony == 'true':
        filter_params['balcony'] = True
    if animalsAllowed == 'true':
        getAnimalsAllowed = AnimalsAllowed.objects.get(status='Tilladt')
        filter_params['animalsAllowed'] = getAnimalsAllowed
    if elevator == 'true':
        filter_params['elevator'] = True
    if furnished == 'true':
        filter_params['furnished'] = True
    if parking == 'true':
        filter_params['parking'] = True

    # Apply filters based on user input
    filtered_results = RentalApartment.objects.filter(**filter_params).order_by(sortMethod)

    items_per_page = 21  # Adjust as needed
    paginator = Paginator(filtered_results, items_per_page)

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('side')

    # Get the Page object for the current page number
    page = paginator.get_page(page_number)

    # Create a list to hold the formatted HTML elements
    html_elements = []

    # Iterate over each apartment in the filtered results
    for apartment in page:
        timestamp = apartment.timestamp
        time_since = timesince(timestamp)

        # Retrieve the first image for the apartment
        first_image = apartment.apartmentimage_set.first()

        # Generate the HTML for each apartment
        html = f"""
            <div class="col-sm-3 boligAnnonce" style="margin-left:8px; margin-right:8px; display:inline-block;"
                onclick="window.location.href='{reverse('rentalApartment', args=[apartment.id])}'">
                """

        # Check if there is a first image available
        if first_image:
            html += f"""
                <img src="{first_image.images.url}" class="img-fluid" alt="">
            """

        html += f"""
                <h2 class="address">{apartment.title[:20]}..</h2>
                <small style="padding-left: 10px;">{apartment.type}</small>
                <div class="" style="padding-left: 8px; padding-bottom: 5px; font-size:14px; position: absolute; bottom:20px;">
                    <img src="https://www.lejebolig.dk/Content/2015/Images/tinypng/resultat-stat-areal-light.png"
                        style="width:20px;">
                    <span>{apartment.size}</span>
                    <br>
                    <img src="https://www.lejebolig.dk/Content/2015/Images/tinypng/resultat-stat-vaerelser-light.png"
                        style="width:20px;">
                    <span>{apartment.rooms} vær.</span>
                </div>
                <p class="price">{apartment.monthlyRent} kr.</p>
                <p style="display:block; color:#8B8B8B; float:left; font-size:10px; position: absolute; bottom:0px; margin:0px 0px 4px 5px; padding-left: 5px;">
                    {time_since} siden</p>
            </div>
            """

        # Add the HTML element to the list
        html_elements.append(html)

    # Return the filtered results as a JSON response
    return JsonResponse(html_elements, safe=False)

@login_required
def saveApartmentAjax(request, apartmentId):
    myApartment = RentalApartment.objects.get(id=apartmentId)

    savedApartment = SavedApartment.objects.filter(user=request.user, rentalApartment=myApartment)

    if savedApartment.exists():
        response = {'message': 'Removed'}
        savedApartment.delete()
    else:
        SavedApartment.objects.create(user=request.user, rentalApartment=myApartment)
        response = {'message': 'Saved'}

    return JsonResponse(response)

@login_required
def report_rental_apartment_ajax(request, apartmentId):
    if request.method == 'POST':

        if not request.POST.get('title') and request.POST.get('reason'):
            errorResponse = {'message': 'Error'}
            return JsonResponse(errorResponse)

        title = request.POST.get('title')
        reason = request.POST.get('reason')
        myApartment = RentalApartment.objects.get(id=apartmentId)

        ReportRentalApartment.objects.create(rentalApartment=myApartment, user=request.user, title=title, reason=reason)
        response = {'message': 'Reported'}
        return JsonResponse(response)


## Delete on launch
def error404(request):
    return render(request, '404.html')