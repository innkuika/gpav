import os
import requests
from django.core.management.base import BaseCommand
from gpav_app.models import Post, Person, Comment, Poll, PollChoice, Link, Media
from typing import List, Optional
from bs4 import BeautifulSoup
from dateutil import parser
from urllib.parse import unquote