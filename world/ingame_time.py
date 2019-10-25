from evennia.utils import gametime 
from typeclasses.rooms import Room

def at_sunrise():
    """When the sun rises, display a message in every room."""
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("Dark clouds in the air shift above you.")

def at_sunset():
    # Browse all rooms
    for room in Room.objects.all():
        room.msg_contents("A gust of wind blows through the area.")

def start_sunrise_event():
    """Schedule an sunrise event to happen every day at 6 AM."""
    script = gametime.schedule(at_sunrise, repeat=True, hour=6, min=0, sec=0)
    script.key = "flavor 1"

def start_sunset_event():
    script = gametime.schedule(at_sunset, repeat=True, hour=19, min=53, sec=0)
    script.key = "flavor 2"