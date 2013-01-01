###
Hello, you're an inquisitive young one for looking into the source code!
This JavaScript wil look like a mess! It's been generated by CoffeeScript,
If you're here, I'm guessing you wondering how we did some of the things on our site?
I am happy to tell you!
First off, the eye following images work by determining the x,y from the pictures (centers)
to the mouse, when the mouse hovers over the that "About Us" slide.
From that, we do some simple trig. using tans to determine the angles, and use switch cases to add the various classes
needed to tell the "pictures" where to look!

What to know more about the code? Give me a tweet! (Don't be afraid, I compliment you've looked in this code!)
I'm @cameronmaske on Twitter, or pop me an email at c@meronmaske.com
Check out the full source on github! https://github.com/cameronmaske/cameronmaske.com
###

$ -> #When the document is ready and loaded.
	$('body').on "mousemove", (event) ->
		cam = $('#me')

		position = (person) ->
			x = event.pageX - person.offset().left - person.width()/2
			y = event.pageY - person.offset().top - person.height()/2
			rads = Math.atan2(y, x) + Math.PI
			degree = rads / (Math.PI/180)

		change = (position, person, name) ->
			looking = person.data('looking')
			if looking != position
				person.removeClass looking
				person.addClass position
				person.data 'looking', position

		looking_at = (person,degree, name) -> switch
			when degree > 340 or degree < 20
				change "left", person, name
			when degree > 20 and degree < 70
				change "up-left", person, name
			when degree > 70 and degree < 110
				change "up", person, name
			when degree > 110 and degree < 160
				change "up-right", person, name
			when degree > 160 and degree < 200
				change "right", person, name
			when degree > 200 and degree < 250
				change "down-right", person, name
			when degree > 250 and degree < 290
				change "down", person, name
			when degree > 290 and degree < 340
				change "down-left", person, name

		cam_looking = position(cam)
		looking_at(cam, cam_looking, "me")
