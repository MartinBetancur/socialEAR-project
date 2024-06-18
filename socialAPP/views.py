from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from .models import *
from .forms import UserRegisterForm, PostForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
import requests
from django.conf import settings
import urllib.parse
from django.http import JsonResponse
from rest_framework import viewsets, mixins
from .serializers import PostSerializer
import json
from django.http import JsonResponse
import os




# Create your views here.
def feed(request):
	posts = Post.objects.all()

	context = { 'posts': posts}
	return render(request, 'feed.html', context)

def register(request):
	if request.method == 'POST':
		form = UserRegisterForm(request.POST)
		if form.is_valid():
			login(request,form.save())

			username = form.cleaned_data['username']
			messages.success(request, f'Usuario {username} creado')
			return redirect('feed')
	else:
		form = UserRegisterForm()

	context = { 'form' : form }
	return render(request, 'register.html', context)

@login_required
def post(request):
	current_user = get_object_or_404(User, pk=request.user.pk)
	if request.method == 'POST':
		form = PostForm(request.POST, request.FILES)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = current_user
			post.save()
			messages.success(request, 'Post enviado')
			return redirect('feed')
	else:
		form = PostForm()
	return render(request, 'post.html', {'form' : form })



def profile(request, username=None):
	current_user = request.user
	if username and username != current_user.username:
		user = User.objects.get(username=username)
		posts = user.posts.all()
	else:
		posts = current_user.posts.all()
		user = current_user
	return render(request, 'profile.html', {'user':user, 'posts':posts})


def follow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user
	rel = Relationship(from_user=current_user, to_user=to_user_id)
	rel.save()
	messages.success(request, f'sigues a {username}')
	return redirect('feed')

def unfollow(request, username):
	current_user = request.user
	to_user = User.objects.get(username=username)
	to_user_id = to_user.id
	rel = Relationship.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
	rel.delete()
	messages.success(request, f'Ya no sigues a {username}')
	return redirect('feed')

def keyword(request):
	return render(request, 'keyword.html')

def index(request):
	return render(request, 'index.html')

def profilefront(request):
	return render(request, 'profile-front.html')

def logouto(request):
	if request.method == 'POST':
		print("Hola")
		logout(request)
	return redirect("index")

def editProfile(request):
	return render(request, "edit-profile.html")


#Linkedin API
def linkedin_post(request):
	# URL del perfil de LinkedIn del usuario del cual deseas obtener los posts
	linkedin_url = "https://www.linkedin.com/in/martinbetancurarango"

	# Codificar la URL de LinkedIn para que sea segura para incluirla en la solicitud
	encoded_linkedin_url = urllib.parse.quote(linkedin_url, safe='')

	# Construir la URL completa para la solicitud a la API de Lix
	url = f"https://api.lix-it.com/v1/li/linkedin/search/posts?url={encoded_linkedin_url}"

	# API key proporcionada por Lix para autenticación
	lix_api_key = 'xvawij6bnpeyLxK5BZ6I63pKKFN2x7pjn4OgEQK9kxW1zdOnf2DKZuwaUGgp'

	# Headers de la solicitud con la API key para autenticación
	headers = {'Authorization': lix_api_key}

	# Realizar la solicitud GET a la API de Lix
	# response = requests.get(url, headers=headers)

	# Verificar si la solicitud fue exitosa y devolver los posts como respuesta JSON
	# result = response.json()
	
	# Simla las variables
	response = {'status_code': 200}
	result = {
		"meta": {
			"sequenceId": "4365746a-3dde-4109-b296-7735b343dac0"
		},
		"paging": {
			"count": 10,
			"start": 0,
			"total": 403
		},
		"posts": [
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/sync/C4E12AQGNpPeWgVqPyQ/article-cover_image-shrink_423_752/0/1520217486881?e=1720656000&v=beta&t=hOV1WvFTfwvThHZbCtYU0OT7tl5-5bLV8uJjqBB5yqE",
				"source": "Neha Desai on LinkedIn",
				"title": "6 years at Linkedin!"
			},
			"id": "6077195953964662784",
			"numComments": 23,
			"numReactions": [
				{
				"count": 140,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "Senior Engineering Manager at Apple",
				"link": "https://www.linkedin.com/in/ACoAAAADQE0BD_IFZTmKdMqY-kPXsSTKd8__Qcg?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAADQE0BD_IFZTmKdMqY-kPXsSTKd8__Qcg",
				"name": "Neha Desai"
			},
			"postedAt": "2015-05-09T02:24:53.182093097Z",
			"urn": "urn:li:activity:6077195953964662784"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/C4D12AQHocgeH8f7bew/article-cover_image-shrink_423_752/0/1580432608254?e=1720656000&v=beta&t=6f40oqtDyItSMrN-ynaMwFTJMVYfpamJEBdBVJfWv7U",
				"source": "Akhilesh Gupta on LinkedIn",
				"title": "Managing EventSource connections with Akka Actors in Play 2.8"
			},
			"id": "6628815814873100288",
			"numComments": 2,
			"numReactions": [
				{
				"count": 28,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"count": 2,
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"numShares": 1,
			"person": {
				"description": "Making LinkedIn ⚡️ fast!",
				"link": "https://www.linkedin.com/in/ACoAAAL-omMBOteJFBOTlXw6exnQaKJgQosYNOw?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAL-omMBOteJFBOTlXw6exnQaKJgQosYNOw",
				"name": "Akhilesh Gupta"
			},
			"postedAt": "2020-05-07T02:24:53.182155153Z",
			"text": "Learn how to use Akka Streams to manage persistent connections on the Play Framework in my first technical post on LinkedIn. #akka #playframework #eventsource #linkedin #engineering",
			"urn": "urn:li:activity:6628815814873100288"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/D5612AQHcpi9oNXasdg/article-cover_image-shrink_423_752/0/1714944593439?e=1720656000&v=beta&t=rTokecMVLYcjDi49AoG8lw1CRgHa5ownHGHqLNldDjY",
				"source": "Peter J. Merrick, TEP on LinkedIn",
				"title": "Excess Mortality"
			},
			"id": "7192999330687979520",
			"numComments": 5,
			"numReactions": [
				{
				"count": 18,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"count": 3,
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"numShares": 6,
			"person": {
				"description": "Commentator/Keynote Speaker & Expert in US/ International Cross Border Insurance & Annuity Planning - Author of The Business Novel - The King of Main Street - Peter@PeterMerrick.com",
				"link": "https://www.linkedin.com/in/ACoAAAEAsyABcaqbIbWhYZg1das-Aq5behUIvSQ?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEAsyABcaqbIbWhYZg1das-Aq5behUIvSQ",
				"name": "Peter J. Merrick, TEP"
			},
			"postedAt": "2024-05-05T22:24:53.182165947Z",
			"text": "Excess Mortality: Life Insurance Sector Concerned Over Prolonged Excess Mortality Rates: The life insurance sector is facing mounting concern, as alarming excess mortality rates continue to potentially impact earnings and elevate death claims.\n\nExcess mortality, as defined, denotes the disparity between the observed number of deaths during a specified timeframe and the anticipated number. During the pandemic's outbreak, a rise in these numbers was anticipated. However, there's a growing apprehension among industry experts and health officials regarding the rate's persistence even as COVID-19 infection numbers wane.\n\nTo continue reading this post, click the graph below and sign-up for the LinkedIn Newsletter - The King of Main Street",
			"urn": "urn:li:activity:7192999330687979520"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/sync/C4D12AQEawkH3RjZjQw/article-cover_image-shrink_423_752/0/1520137887549?e=1720656000&v=beta&t=NK0jwaO7R3yjZH8DULdX1puhyKYjY_Jc4r4i1dUESKM",
				"source": "Asif Makhani on LinkedIn",
				"title": "Revolutionizing education through LinkedIn Learning"
			},
			"id": "6184957676598870016",
			"numComments": 21,
			"numReactions": [
				{
				"count": 169,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "Tech Exec",
				"link": "https://www.linkedin.com/in/ACoAAAASoc8B3xDIYty0hgJi-zRSVjo85roCmgE?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAASoc8B3xDIYty0hgJi-zRSVjo85roCmgE",
				"name": "Asif Makhani"
			},
			"postedAt": "2016-05-08T02:24:53.182413160Z",
			"text": "#LinkedInLearning live!",
			"urn": "urn:li:activity:6184957676598870016"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/D5612AQGWgGRSQ6CLsA/article-cover_image-shrink_423_752/0/1711488066568?e=1720656000&v=beta&t=0L6Otj7n9IdP8hKenAsIpXcPRcaGWKVunJnMw2uRQQ0",
				"source": "Jeff Frick on LinkedIn",
				"title": "I asked ChatGPT to fill my brackets"
			},
			"id": "7178544313746776064",
			"numComments": 19,
			"numReactions": [
				{
				"count": 19,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"count": 2,
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"numShares": 3,
			"person": {
				"description": "Engagement Engineer | Community Builder | Linked Top Voice | Video Virtuoso | Content Curator | Host, Turn the Lens podcast and Work 20XX podcast",
				"link": "https://www.linkedin.com/in/ACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA",
				"name": "Jeff Frick"
			},
			"postedAt": "2024-04-06T02:24:53.182433075Z",
			"text": "I asked ChatGPT to fill in my brackets\nHere's how it went, and how it's going, and all the bits in between.\n\n(ChatGPT, make me a hashtag cloud that encapsulates our conversation) \n\nFor a hashtag cloud related to our conversation and the process of working together, especially if you're aiming to share insights on LinkedIn about March Madness predictions and the analytical approach towards the NCAA tournaments, consider using a mix of general, topic-specific, and process-oriented hashtags. Here's a suggestion that encapsulates the breadth of our discussion:\n\nThis cloud mixes specific event hashtags (#MarchMadness2024, #NCAATournament, #NCAAWomen) with those highlighting the analytical process (#BracketAnalysis, #PredictiveAnalytics, #BasketballAnalytics) and the collaborative nature of our interaction (#CollaborativeAnalysis, #PartnershipSuccess, #SharedGoals). Additionally, it touches on broader themes like women's sports (#WomenInSports, #EmpowermentThroughSports), strategic thinking (#StrategicThinking, #DataDrivenDecisions), and outcomes of our discussions (#InsightsDiscovery, #AchievementUnlocked).\n\nThese hashtags are designed to capture the essence of our conversation, the analytical approach towards tournament predictions, and the value of teamwork and shared insights in navigating complex challenges. Sharing with these hashtags on LinkedIn can help categorize your post for broader visibility among professionals interested in sports analytics, strategic planning, and women's basketball.\n\n#MarchMadness2024 #NCAATournament #BracketAnalysis #WomenInSports #BasketballAnalytics #PredictiveAnalytics #ai #genai #openai #chatgpt #hoops #basketball Bill #SportsStrategy #newsletter #anitaiverson #TeamPerformance #GameByGame #UpsetAlerts #FinalFourPredictions #ChampionshipMindset #CollaborativeAnalysis #InsightsDiscovery #StrategicThinking #DataDrivenDecisions #topvoice #LinkedInNewsLetters #NCAAWomen #EmpowermentThroughSports #LeadershipInSports #InnovationInAnalytics #PartnershipSuccess #SharedGoals #AchievementUnlocked ",
			"urn": "urn:li:activity:7178544313746776064"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/sync/C4E12AQFjO5eBsUdj-w/article-cover_image-shrink_423_752/0/1520236121758?e=1720656000&v=beta&t=uIvGUY-R7nZDPsyfKpdJAD4Wfk0l46wMNYDxprQ_1sQ",
				"source": "Satya Nadella on LinkedIn",
				"title": "Microsoft + LinkedIn: Beginning our Journey Together"
			},
			"id": "6212627171396153344",
			"numComments": 369,
			"numReactions": [
				{
				"count": 9690,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"count": 1,
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "Chairman and CEO at Microsoft",
				"link": "https://www.linkedin.com/in/ACoAAAEkwwAB9KEc2TrQgOLEQ-vzRyZeCDyc6DQ?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEkwwAB9KEc2TrQgOLEQ-vzRyZeCDyc6DQ",
				"name": "Satya Nadella"
			},
			"postedAt": "2016-05-08T02:24:53.182444188Z",
			"urn": "urn:li:activity:6212627171396153344"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/D5612AQEyz4cICwV6jg/article-cover_image-shrink_423_752/0/1714961097549?e=1720656000&v=beta&t=cP7gcpd_HRvKzlf-AwyoI2FeUqBMUhsd96j9s3qOfGQ",
				"source": "Md. Abdur Razzak on LinkedIn",
				"title": "LinkedIn Success Blueprint: Strategies for Growth"
			},
			"id": "7193068825825665024",
			"numReactions": [
				{
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "Advanced Digital Marketing Manager | Virtual Assistant | Certified Social Media Marketing | Article Writing",
				"link": "https://www.linkedin.com/in/ACoAADcB-G0BA1cvNv4McgMAue_ek5DA0DILvHM?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADcB-G0BA1cvNv4McgMAue_ek5DA0DILvHM",
				"name": "Md. Abdur Razzak"
			},
			"postedAt": "2024-05-06T02:07:53.182452049Z",
			"text": "LinkedIn Success Blueprint: Strategies for Growth 👇 \n\n\n\n\n✍ \nIn the vast landscape of professional networking, LinkedIn stands out as the go-to platform for connecting with like-minded individuals, expanding career opportunities, and nurturing professional growth. With over 700 million members worldwide, LinkedIn offers a goldmine of potential for those who know how to harness its power effectively. In this comprehensive guide, we'll delve into the strategies and tactics you need to cultivate a thriving presence on LinkedIn and propel your career to new heights.\n\nBy implementing these strategies and tactics, you can unlock the full potential of LinkedIn as a tool for professional growth and success. Whether you're looking to advance your career, expand your network, or establish yourself as a thought leader in your industry, LinkedIn offers a wealth of opportunities for those willing to invest the time and effort. So, roll up your sleeves, optimize your profile, start engaging with your network, and watch as your LinkedIn presence flourishes, opening doors to new opportunities and connections along the way.",
			"urn": "urn:li:activity:7193068825825665024"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/D5612AQFu9VwrHGsGiQ/article-cover_image-shrink_423_752/0/1711122678029?e=1720656000&v=beta&t=qaq3W8BohHPOX9Qv-bC-uLIcN91LoTpJg1bATk3C7Cg",
				"source": "Jeff Frick on LinkedIn",
				"title": "• Hackers • Meetings • F-Word • Swirls • Multiply •"
			},
			"id": "7176970562362073091",
			"numReactions": [
				{
				"count": 18,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"count": 3,
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"numShares": 1,
			"person": {
				"description": "Engagement Engineer | Community Builder | Linked Top Voice | Video Virtuoso | Content Curator | Host, Turn the Lens podcast and Work 20XX podcast",
				"link": "https://www.linkedin.com/in/ACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA",
				"name": "Jeff Frick"
			},
			"postedAt": "2024-04-06T02:24:53.182460489Z",
			"text": "• Hackers • Meetings • F-Word • Swirls • Multiply • \n\nHow's your bracket? What's a Bracket? Happy Friday either way. \n\nTime to hit \"Publish\" and send you this week's edition of the Friday Five, five posts that touched a nerve.\n \nIf you enjoy the Friday Five, please drop a comment, share with a friend, and follow on Spotify and YouTube. \nThanks for your community!\nHappy Friday. \n\n#Hackers #Meetings #FWord #Swirls #Multiply #FridayFive #TurnTheLens #Work20XX #Adaptability #agency #AI #AIandCybersecurity #Ambiguity #Analytics #atlassian #Atlassian #Automotive #AutotechCouncil #BeyondBoxes #BigCo #BigCompanies #bigtrend #bond #box #Brackets #BreakingBoundaries #breakthrough #BritishTelecom #bulls #Business #captioned #cars #CEO #Champion #championship #Change #CIO #CleanTech #CleantechCouncil #Collaboration #connect #Connection #Connections #ContinuousLearning #culture #curiosity #cxo #CybersecurityInsights #Data #DataCentric #Dean #DeanOfBigData #decisions #Digital #digital #DigitalTransformation #Digitization #distributed #electric #ElectricVehicles #EmbracingFeel #empathy #empower #Empowerment #Energy #EthicalHacking #ev #exercise #exponential #Feel #FeelFactor #feelliketherightthing #findfertile #FindFertileGround #flexible #forcemultiplier #forrest #fow #freshair #futureofwork #Goodhartslaws #GreenTech #grow #GrowAForrest #Growth #HackerOne #hoops #host #houston #howtowork #human #hybrid #Improvisation #Innovating #Innovation #InnovationInTech #intentional #interview #iowa #Jam #Jazz #JazzQuartetApproach #JohnPaxson #KertonGroup #Leadership #LeadershipLessons #Leading #learning #Learning #LevelUpYourLI #LinkedInLive #LIVideo #madness #MarchMadness #marginalimprovement #measures #meeting #Mentoring #MichaelJordan #MindsetShift #MobileInternet #multipletrends #NCAA #NokiaVenturePartners #office #OfficePool #Organization #OrganizationalImprovisation #People #plantaseed #podcast #productivity #PsychologicalSafety #radicaltransparency #remote #rto #safety #Scale #security #SecurityTrends #SiliconValley #Skills #SKTelecom #SmallCo #StartUp #Startups #SteveKerr #Success #Swisscom #takeawalk #Teach #Team #TeamBuilding #TeamDynamics #Teamwork #tech #Tech #TechLeadership #TechnologicalTrends #Technology #TechnologyTrends #Telcos #TelecomCompany #TelecomCouncil #thefuture #time #TopVoice #Tournament #Training #transparency #trends #trust #Trust #VC #Venture #VentureCapital #walk #walkabout #work #workplace",
			"urn": "urn:li:activity:7176970562362073091"
			},
			{
			"embeddedObject": {

			},
			"id": "7177027767299887104",
			"numComments": 8,
			"numReactions": [
				{
				"count": 48,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"count": 2,
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"count": 3,
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "CEO at Truv | Open Finance Platform For Lenders",
				"link": "https://www.linkedin.com/in/ACoAAAM4ksUB_E7e9j05ht2AHwFA7aGahWMTpcE?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAM4ksUB_E7e9j05ht2AHwFA7aGahWMTpcE",
				"name": "Kirill Klokov"
			},
			"postedAt": "2024-04-06T02:24:53.182467821Z",
			"text": "Our first prototype of Truv was a piece of software I wouldn’t be proud of today.\n\nIt was June 2020 and we were cold emailing lenders on LinkedIn.\n\nPretty quickly, we had a few sales calls.\n\n30 minutes into a call, a lender interrupted us and offered us $60k for a subscription and asked for six-month exclusivity.\n\nAnd he wanted to invest in the company (that we hadn’t even set up yet).\n\nFor a proof-of-concept product connected to ADP.\n\nThat we weren’t very proud of.\n\nYou almost never get such clear signals from the market.\n\nSo we doubled down on this space:\n- Established market\n- Few disrupters\n- Solve a big pain point\n- Selling picks and shovels\n- Insulated from market volatility\n\nToday we feel we’re on path to unseating our biggest competitor.\n\nA lot can change in 4 years in the startup world.\n",
			"urn": "urn:li:activity:7177027767299887104"
			},
			{
			"embeddedObject": {
				"imageUrl": "https://media.licdn.com/dms/image/D4E12AQHMxDa3nYpwXg/article-cover_image-shrink_423_752/0/1714934598201?e=1720656000&v=beta&t=mie19xjCcrYQKIsEFrpyatEzNGHr1qUhQirb75p9mEI",
				"source": "Rory O'Gallagher on LinkedIn",
				"title": "Bridging Surveys and Conversations with Generative Listening Tools"
			},
			"id": "7192966220059471872",
			"numComments": 5,
			"numReactions": [
				{
				"count": 18,
				"reactionType": "REACTION_TYPE_LIKE"
				},
				{
				"reactionType": "REACTION_TYPE_PRAISE"
				},
				{
				"reactionType": "REACTION_TYPE_INTEREST"
				},
				{
				"count": 2,
				"reactionType": "REACTION_TYPE_EMPATHY"
				}
			],
			"person": {
				"description": "Sr. Behavioral Scientist @ GE HealthCare | Collaboration, Productivity & Culture",
				"link": "https://www.linkedin.com/in/ACoAAAvnJFkBm9KwC1g5OXxYwdUAnQ6ET3DM8k8?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAvnJFkBm9KwC1g5OXxYwdUAnQ6ET3DM8k8",
				"name": "Rory O'Gallagher"
			},
			"postedAt": "2024-05-05T19:24:53.182473773Z",
			"text": "Hey LinkedIn Network, I wrote my first blog post! This was a personal goal I've been putting off for quite some time. Some of Richard Rosenow's writing inspired this post about generative listening. Rich, thanks for encouraging me to just get something out there.\n\nFor anyone interested in reading, please share your impressions and feedback. I am writing as a way to connect with others and learn from their experience. I appreciate any feedback as a way to inform my opinions and hope to make some new friends in the people analytics space from this hobby.  #employeelistening #peopleanalytics ",
			"urn": "urn:li:activity:7192966220059471872"
			}
		]
	}
	
	print("result", result)
	if response['status_code'] == 200:
		return render(request, "linkedin_post.html", { 'result': result } )
		# return JsonResponse(result)
	else:
		# Si la solicitud no fue exitosa, devolver un mensaje de error con el código de estado
		return render(request, "linkedin_post.html", { 'error': True, 'status_code': response['status_code'], 'result': result } )


#API KEY - aRVzjlw36uBwvdb1pTruhVbTW3HXHnt8LJpmAqNdKpaS9ydN0B6ZjxSgQTwp


posts_json = {
	"meta": {
    "sequenceId": "4365746a-3dde-4109-b296-7735b343dac0"
},
"paging": {
    "count": 10,
    "start": 0,
    "total": 403
},
"posts": [
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/sync/C4E12AQGNpPeWgVqPyQ/article-cover_image-shrink_423_752/0/1520217486881?e=1720656000&v=beta&t=hOV1WvFTfwvThHZbCtYU0OT7tl5-5bLV8uJjqBB5yqE",
        "source": "Neha Desai on LinkedIn",
        "title": "6 years at Linkedin!"
    },
    "id": "6077195953964662784",
    "numComments": 23,
    "numReactions": [
        {
        "count": 140,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "Senior Engineering Manager at Apple",
        "link": "https://www.linkedin.com/in/ACoAAAADQE0BD_IFZTmKdMqY-kPXsSTKd8__Qcg?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAADQE0BD_IFZTmKdMqY-kPXsSTKd8__Qcg",
        "name": "Neha Desai"
    },
    "postedAt": "2015-05-09T02:24:53.182093097Z",
    "urn": "urn:li:activity:6077195953964662784"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/C4D12AQHocgeH8f7bew/article-cover_image-shrink_423_752/0/1580432608254?e=1720656000&v=beta&t=6f40oqtDyItSMrN-ynaMwFTJMVYfpamJEBdBVJfWv7U",
        "source": "Akhilesh Gupta on LinkedIn",
        "title": "Managing EventSource connections with Akka Actors in Play 2.8"
    },
    "id": "6628815814873100288",
    "numComments": 2,
    "numReactions": [
        {
        "count": 28,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "count": 2,
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "numShares": 1,
    "person": {
        "description": "Making LinkedIn ⚡️ fast!",
        "link": "https://www.linkedin.com/in/ACoAAAL-omMBOteJFBOTlXw6exnQaKJgQosYNOw?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAL-omMBOteJFBOTlXw6exnQaKJgQosYNOw",
        "name": "Akhilesh Gupta"
    },
    "postedAt": "2020-05-07T02:24:53.182155153Z",
    "text": "Learn how to use Akka Streams to manage persistent connections on the Play Framework in my first technical post on LinkedIn. #akka #playframework #eventsource #linkedin #engineering",
    "urn": "urn:li:activity:6628815814873100288"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/D5612AQHcpi9oNXasdg/article-cover_image-shrink_423_752/0/1714944593439?e=1720656000&v=beta&t=rTokecMVLYcjDi49AoG8lw1CRgHa5ownHGHqLNldDjY",
        "source": "Peter J. Merrick, TEP on LinkedIn",
        "title": "Excess Mortality"
    },
    "id": "7192999330687979520",
    "numComments": 5,
    "numReactions": [
        {
        "count": 18,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "count": 3,
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "numShares": 6,
    "person": {
        "description": "Commentator/Keynote Speaker & Expert in US/ International Cross Border Insurance & Annuity Planning - Author of The Business Novel - The King of Main Street - Peter@PeterMerrick.com",
        "link": "https://www.linkedin.com/in/ACoAAAEAsyABcaqbIbWhYZg1das-Aq5behUIvSQ?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEAsyABcaqbIbWhYZg1das-Aq5behUIvSQ",
        "name": "Peter J. Merrick, TEP"
    },
    "postedAt": "2024-05-05T22:24:53.182165947Z",
    "text": "Excess Mortality: Life Insurance Sector Concerned Over Prolonged Excess Mortality Rates: The life insurance sector is facing mounting concern, as alarming excess mortality rates continue to potentially impact earnings and elevate death claims.\n\nExcess mortality, as defined, denotes the disparity between the observed number of deaths during a specified timeframe and the anticipated number. During the pandemic's outbreak, a rise in these numbers was anticipated. However, there's a growing apprehension among industry experts and health officials regarding the rate's persistence even as COVID-19 infection numbers wane.\n\nTo continue reading this post, click the graph below and sign-up for the LinkedIn Newsletter - The King of Main Street",
    "urn": "urn:li:activity:7192999330687979520"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/sync/C4D12AQEawkH3RjZjQw/article-cover_image-shrink_423_752/0/1520137887549?e=1720656000&v=beta&t=NK0jwaO7R3yjZH8DULdX1puhyKYjY_Jc4r4i1dUESKM",
        "source": "Asif Makhani on LinkedIn",
        "title": "Revolutionizing education through LinkedIn Learning"
    },
    "id": "6184957676598870016",
    "numComments": 21,
    "numReactions": [
        {
        "count": 169,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "Tech Exec",
        "link": "https://www.linkedin.com/in/ACoAAAASoc8B3xDIYty0hgJi-zRSVjo85roCmgE?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAASoc8B3xDIYty0hgJi-zRSVjo85roCmgE",
        "name": "Asif Makhani"
    },
    "postedAt": "2016-05-08T02:24:53.182413160Z",
    "text": "#LinkedInLearning live!",
    "urn": "urn:li:activity:6184957676598870016"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/D5612AQGWgGRSQ6CLsA/article-cover_image-shrink_423_752/0/1711488066568?e=1720656000&v=beta&t=0L6Otj7n9IdP8hKenAsIpXcPRcaGWKVunJnMw2uRQQ0",
        "source": "Jeff Frick on LinkedIn",
        "title": "I asked ChatGPT to fill my brackets"
    },
    "id": "7178544313746776064",
    "numComments": 19,
    "numReactions": [
        {
        "count": 19,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "count": 2,
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "numShares": 3,
    "person": {
        "description": "Engagement Engineer | Community Builder | Linked Top Voice | Video Virtuoso | Content Curator | Host, Turn the Lens podcast and Work 20XX podcast",
        "link": "https://www.linkedin.com/in/ACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA",
        "name": "Jeff Frick"
    },
    "postedAt": "2024-04-06T02:24:53.182433075Z",
    "text": "I asked ChatGPT to fill in my brackets\nHere's how it went, and how it's going, and all the bits in between.\n\n(ChatGPT, make me a hashtag cloud that encapsulates our conversation) \n\nFor a hashtag cloud related to our conversation and the process of working together, especially if you're aiming to share insights on LinkedIn about March Madness predictions and the analytical approach towards the NCAA tournaments, consider using a mix of general, topic-specific, and process-oriented hashtags. Here's a suggestion that encapsulates the breadth of our discussion:\n\nThis cloud mixes specific event hashtags (#MarchMadness2024, #NCAATournament, #NCAAWomen) with those highlighting the analytical process (#BracketAnalysis, #PredictiveAnalytics, #BasketballAnalytics) and the collaborative nature of our interaction (#CollaborativeAnalysis, #PartnershipSuccess, #SharedGoals). Additionally, it touches on broader themes like women's sports (#WomenInSports, #EmpowermentThroughSports), strategic thinking (#StrategicThinking, #DataDrivenDecisions), and outcomes of our discussions (#InsightsDiscovery, #AchievementUnlocked).\n\nThese hashtags are designed to capture the essence of our conversation, the analytical approach towards tournament predictions, and the value of teamwork and shared insights in navigating complex challenges. Sharing with these hashtags on LinkedIn can help categorize your post for broader visibility among professionals interested in sports analytics, strategic planning, and women's basketball.\n\n#MarchMadness2024 #NCAATournament #BracketAnalysis #WomenInSports #BasketballAnalytics #PredictiveAnalytics #ai #genai #openai #chatgpt #hoops #basketball Bill #SportsStrategy #newsletter #anitaiverson #TeamPerformance #GameByGame #UpsetAlerts #FinalFourPredictions #ChampionshipMindset #CollaborativeAnalysis #InsightsDiscovery #StrategicThinking #DataDrivenDecisions #topvoice #LinkedInNewsLetters #NCAAWomen #EmpowermentThroughSports #LeadershipInSports #InnovationInAnalytics #PartnershipSuccess #SharedGoals #AchievementUnlocked ",
    "urn": "urn:li:activity:7178544313746776064"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/sync/C4E12AQFjO5eBsUdj-w/article-cover_image-shrink_423_752/0/1520236121758?e=1720656000&v=beta&t=uIvGUY-R7nZDPsyfKpdJAD4Wfk0l46wMNYDxprQ_1sQ",
        "source": "Satya Nadella on LinkedIn",
        "title": "Microsoft + LinkedIn: Beginning our Journey Together"
    },
    "id": "6212627171396153344",
    "numComments": 369,
    "numReactions": [
        {
        "count": 9690,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "count": 1,
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "Chairman and CEO at Microsoft",
        "link": "https://www.linkedin.com/in/ACoAAAEkwwAB9KEc2TrQgOLEQ-vzRyZeCDyc6DQ?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAEkwwAB9KEc2TrQgOLEQ-vzRyZeCDyc6DQ",
        "name": "Satya Nadella"
    },
    "postedAt": "2016-05-08T02:24:53.182444188Z",
    "urn": "urn:li:activity:6212627171396153344"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/D5612AQEyz4cICwV6jg/article-cover_image-shrink_423_752/0/1714961097549?e=1720656000&v=beta&t=cP7gcpd_HRvKzlf-AwyoI2FeUqBMUhsd96j9s3qOfGQ",
        "source": "Md. Abdur Razzak on LinkedIn",
        "title": "LinkedIn Success Blueprint: Strategies for Growth"
    },
    "id": "7193068825825665024",
    "numReactions": [
        {
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "Advanced Digital Marketing Manager | Virtual Assistant | Certified Social Media Marketing | Article Writing",
        "link": "https://www.linkedin.com/in/ACoAADcB-G0BA1cvNv4McgMAue_ek5DA0DILvHM?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAADcB-G0BA1cvNv4McgMAue_ek5DA0DILvHM",
        "name": "Md. Abdur Razzak"
    },
    "postedAt": "2024-05-06T02:07:53.182452049Z",
    "text": "LinkedIn Success Blueprint: Strategies for Growth 👇 \n\n\n\n\n✍ \nIn the vast landscape of professional networking, LinkedIn stands out as the go-to platform for connecting with like-minded individuals, expanding career opportunities, and nurturing professional growth. With over 700 million members worldwide, LinkedIn offers a goldmine of potential for those who know how to harness its power effectively. In this comprehensive guide, we'll delve into the strategies and tactics you need to cultivate a thriving presence on LinkedIn and propel your career to new heights.\n\nBy implementing these strategies and tactics, you can unlock the full potential of LinkedIn as a tool for professional growth and success. Whether you're looking to advance your career, expand your network, or establish yourself as a thought leader in your industry, LinkedIn offers a wealth of opportunities for those willing to invest the time and effort. So, roll up your sleeves, optimize your profile, start engaging with your network, and watch as your LinkedIn presence flourishes, opening doors to new opportunities and connections along the way.",
    "urn": "urn:li:activity:7193068825825665024"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/D5612AQFu9VwrHGsGiQ/article-cover_image-shrink_423_752/0/1711122678029?e=1720656000&v=beta&t=qaq3W8BohHPOX9Qv-bC-uLIcN91LoTpJg1bATk3C7Cg",
        "source": "Jeff Frick on LinkedIn",
        "title": "• Hackers • Meetings • F-Word • Swirls • Multiply •"
    },
    "id": "7176970562362073091",
    "numReactions": [
        {
        "count": 18,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "count": 3,
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "numShares": 1,
    "person": {
        "description": "Engagement Engineer | Community Builder | Linked Top Voice | Video Virtuoso | Content Curator | Host, Turn the Lens podcast and Work 20XX podcast",
        "link": "https://www.linkedin.com/in/ACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAABMvMBoII_2Pm5k4GaDEHCFfdruyo6jrA",
        "name": "Jeff Frick"
    },
    "postedAt": "2024-04-06T02:24:53.182460489Z",
    "text": "• Hackers • Meetings • F-Word • Swirls • Multiply • \n\nHow's your bracket? What's a Bracket? Happy Friday either way. \n\nTime to hit \"Publish\" and send you this week's edition of the Friday Five, five posts that touched a nerve.\n \nIf you enjoy the Friday Five, please drop a comment, share with a friend, and follow on Spotify and YouTube. \nThanks for your community!\nHappy Friday. \n\n#Hackers #Meetings #FWord #Swirls #Multiply #FridayFive #TurnTheLens #Work20XX #Adaptability #agency #AI #AIandCybersecurity #Ambiguity #Analytics #atlassian #Atlassian #Automotive #AutotechCouncil #BeyondBoxes #BigCo #BigCompanies #bigtrend #bond #box #Brackets #BreakingBoundaries #breakthrough #BritishTelecom #bulls #Business #captioned #cars #CEO #Champion #championship #Change #CIO #CleanTech #CleantechCouncil #Collaboration #connect #Connection #Connections #ContinuousLearning #culture #curiosity #cxo #CybersecurityInsights #Data #DataCentric #Dean #DeanOfBigData #decisions #Digital #digital #DigitalTransformation #Digitization #distributed #electric #ElectricVehicles #EmbracingFeel #empathy #empower #Empowerment #Energy #EthicalHacking #ev #exercise #exponential #Feel #FeelFactor #feelliketherightthing #findfertile #FindFertileGround #flexible #forcemultiplier #forrest #fow #freshair #futureofwork #Goodhartslaws #GreenTech #grow #GrowAForrest #Growth #HackerOne #hoops #host #houston #howtowork #human #hybrid #Improvisation #Innovating #Innovation #InnovationInTech #intentional #interview #iowa #Jam #Jazz #JazzQuartetApproach #JohnPaxson #KertonGroup #Leadership #LeadershipLessons #Leading #learning #Learning #LevelUpYourLI #LinkedInLive #LIVideo #madness #MarchMadness #marginalimprovement #measures #meeting #Mentoring #MichaelJordan #MindsetShift #MobileInternet #multipletrends #NCAA #NokiaVenturePartners #office #OfficePool #Organization #OrganizationalImprovisation #People #plantaseed #podcast #productivity #PsychologicalSafety #radicaltransparency #remote #rto #safety #Scale #security #SecurityTrends #SiliconValley #Skills #SKTelecom #SmallCo #StartUp #Startups #SteveKerr #Success #Swisscom #takeawalk #Teach #Team #TeamBuilding #TeamDynamics #Teamwork #tech #Tech #TechLeadership #TechnologicalTrends #Technology #TechnologyTrends #Telcos #TelecomCompany #TelecomCouncil #thefuture #time #TopVoice #Tournament #Training #transparency #trends #trust #Trust #VC #Venture #VentureCapital #walk #walkabout #work #workplace",
    "urn": "urn:li:activity:7176970562362073091"
    },
    {
    "embeddedObject": {

    },
    "id": "7177027767299887104",
    "numComments": 8,
    "numReactions": [
        {
        "count": 48,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "count": 2,
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "count": 3,
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "CEO at Truv | Open Finance Platform For Lenders",
        "link": "https://www.linkedin.com/in/ACoAAAM4ksUB_E7e9j05ht2AHwFA7aGahWMTpcE?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAM4ksUB_E7e9j05ht2AHwFA7aGahWMTpcE",
        "name": "Kirill Klokov"
    },
    "postedAt": "2024-04-06T02:24:53.182467821Z",
    "text": "Our first prototype of Truv was a piece of software I wouldn’t be proud of today.\n\nIt was June 2020 and we were cold emailing lenders on LinkedIn.\n\nPretty quickly, we had a few sales calls.\n\n30 minutes into a call, a lender interrupted us and offered us $60k for a subscription and asked for six-month exclusivity.\n\nAnd he wanted to invest in the company (that we hadn’t even set up yet).\n\nFor a proof-of-concept product connected to ADP.\n\nThat we weren’t very proud of.\n\nYou almost never get such clear signals from the market.\n\nSo we doubled down on this space:\n- Established market\n- Few disrupters\n- Solve a big pain point\n- Selling picks and shovels\n- Insulated from market volatility\n\nToday we feel we’re on path to unseating our biggest competitor.\n\nA lot can change in 4 years in the startup world.\n",
    "urn": "urn:li:activity:7177027767299887104"
    },
    {
    "embeddedObject": {
        "imageUrl": "https://media.licdn.com/dms/image/D4E12AQHMxDa3nYpwXg/article-cover_image-shrink_423_752/0/1714934598201?e=1720656000&v=beta&t=mie19xjCcrYQKIsEFrpyatEzNGHr1qUhQirb75p9mEI",
        "source": "Rory O'Gallagher on LinkedIn",
        "title": "Bridging Surveys and Conversations with Generative Listening Tools"
    },
    "id": "7192966220059471872",
    "numComments": 5,
    "numReactions": [
        {
        "count": 18,
        "reactionType": "REACTION_TYPE_LIKE"
        },
        {
        "reactionType": "REACTION_TYPE_PRAISE"
        },
        {
        "reactionType": "REACTION_TYPE_INTEREST"
        },
        {
        "count": 2,
        "reactionType": "REACTION_TYPE_EMPATHY"
        }
    ],
    "person": {
        "description": "Sr. Behavioral Scientist @ GE HealthCare | Collaboration, Productivity & Culture",
        "link": "https://www.linkedin.com/in/ACoAAAvnJFkBm9KwC1g5OXxYwdUAnQ6ET3DM8k8?miniProfileUrn=urn%3Ali%3Afs_miniProfile%3AACoAAAvnJFkBm9KwC1g5OXxYwdUAnQ6ET3DM8k8",
        "name": "Rory O'Gallagher"
    },
    "postedAt": "2024-05-05T19:24:53.182473773Z",
    "text": "Hey LinkedIn Network, I wrote my first blog post! This was a personal goal I've been putting off for quite some time. Some of Richard Rosenow's writing inspired this post about generative listening. Rich, thanks for encouraging me to just get something out there.\n\nFor anyone interested in reading, please share your impressions and feedback. I am writing as a way to connect with others and learn from their experience. I appreciate any feedback as a way to inform my opinions and hope to make some new friends in the people analytics space from this hobby.  #employeelistening #peopleanalytics ",
    "urn": "urn:li:activity:7192966220059471872"
    }
]}


def search_posts(request: HttpRequest):
    posts = posts_json["posts"]
    keyword = request.POST.get('keyword', '')

    if keyword:
        filtered_posts = [
            post for post in posts
            if keyword.lower() in post.get('text', '').lower() or
               keyword.lower() in post['person']['name'].lower()
        ]
    else:
        filtered_posts = posts

    return render(request, 'search.html', {'posts': filtered_posts})