title: Designing a Website <br> Part 1 · Inspriation
date: 2013-05-11
published: false
topic: WEB DESIGN
scripts: ['/static/js/libs/fitvids.js']
intro: In this series of posts, I’ll be talking about building a website design from scratch. In part 1, we will explore some good starting points and helpful tips on getting the feel and mood of your design down.


5 months, 23 files and 3,528 lines of code later my ([for sale][1]) website design is done. This is the [end result.][2]

[<div class="fit-img">
    <img src="/static/img/media/admino-screenshot.png">
</div>](http://wrapbootstrap.com/preview/WB064S498)

With the fruits of my labour finally done, I wanted to share the creation process.
In my next series of posts, I’ll be talking about the process from start to finish.
For anyone curious in web design, hopefully this will provide a few helpful tips for your own design projects.  Just on that note, this is the my general approach (that works well for me) but isn’t the end all (or necessarily best way) to go about designing a site. With that disclaimer in mind, let’s jump into it.
From start to finish

<div class="fit-vid">
    <iframe width="560" height="315" src="http://www.youtube.com/embed/-A3tfevse6A" frameborder="0" allowfullscreen></iframe>
</div>

Before starting work on design, I knew I wanted to documented and capture the process. I threw together a rudimentary script to take a screenshot of the work in progress site every 60 seconds. The timelapse above is the result of many hours of work condensed in 2 short minutes.

Let’s begin with often the hardest part.

Where to start
--------------

I started by thinking about what the goal of the design was.  The goal in the case was to build a theme suited for web applications. Generic enough to handle the barebones of [CRUD operations][3] (possibily the most common use case for web apps) but also the added ability to visualise data. The intent from the get go was to sell this design. I wanted the end product to be friendly enough to set up, customize and tweak to the specific customer’s needs, but without sacrificing the visual appeal. With the goal in mind, my next step was to start setting the mood of the design.

My design scrapbook
-------------------

When browsing the web  every time I come across a design that I find interesting or impressive I’ll take a screenshot of it and store it away like a scrapbook. It’s become a habit.   Ever so often, when feeling uninspired, I’ll flick through through this design  ‘scrapbook’  folder and find a beautiful reference or approach to some sort of design conundrum. In this project’s case, this was my go to point to start formulating the design. My first milestone was to create the equivalent of a mood board (mood boards are great visual tools to set the ‘feel’ of the design you want to achieve). Technically, this was more a mood folder then a board, but it served the exact same purpose.

Below are are some select snippets.


Snippet #1 - [emberjs.com](www.emberjs.com)
------------------------

[<div class="fit-img">
    <img src="/static/img/media/ember-screenshot.png"/>
</div>](http://www.emberjs.com)

[emberjs.com](http://www.emberjs.com) is a really neat site. What particularly stood out to me was the striking contrast between the red diamond textured navigation bar and main page. It’s distinctive and importantly memorable. Colors for me, are one of the some important aspects to creating a lasting impression (good or bad). Designs lacking saturation can be striking but I have never found them to be particularly memorable. This might only be me, but sites that get colors right leave a lasting impression. In this case, I really liked the interplay between of the colors and texture and the way the design shifts your attention to below the navigation bar.


Snippet #2 - [artiery.io](http://artiery.io)
-------------------------------------------

[<div class="fit-img">
    <img src="/static/img/media/artiery-screenshot-2.png">
</div>](http://www.artery.io)

[artery.io](http://www.artery.io) was interesting for two reason. First, their landing page combines clean white typography on dark gray produces a high contrast striking design with great readability.  The touches of color (blue and red) fit in well on the dark background (and make it memorable).

The second reason was the interaction of the sidebar. See the video below

<div class="fit-vid">
    <iframe class="fit-vid" src="http://www.screenr.com/embed/rF37" width="650" height="396" frameborder="0"></iframe>
</div>

It felt intuitive. Hiding when not needed to maximise all space for the users focus, but was easy to call upon when wanted. I really like it’s convenience and wanted to capture that in my own design.

Snippet #3 - [dribbble.com](http://dribbble.com)
------------------------------------------------

[<div class="fit-img">
    <img src="http://dribbble.s3.amazonaws.com/users/5577/screenshots/630596/crm_project_small.png"/>
</div>](http://dribbble.com/shots/630596-CRM-Project-Page)

Dribbble (a network of very talented graphic designers and digital artists from all around the world) is a great bucket of inspiration. After exhausting my ‘scrapbook’ folder, this was my next destination. I really liked the layout of this particular sidebar by Jason Mayo [http://dribbble.com/madebymayo]. The contrast from sidebar to main page is distinct and communicates a clear separation of functionality to user. The active ‘tab’ in the sidebar clearly links to the main page by sharing the same colour. It’s intention is so obvious and intuitive.

With a few ideas in the pipeline, the next step was to begin crafting the UI.

Pen and *paper*
-------------

Before touching any code, I like to prototype any initial ideas with ‘pen and paper’ (in this case, it was with a great iPad app called Paper[http://www.fiftythree.com/paper]). Mockups are great starting points. Any mistakes on paper are cheap and effortless to correct (unlike code). Mockups can also serve as great reference points further down a project’s life. Working top down from a mock up can serve as an effective way to plan what to do next.

The level of detail is a preference and project specific. In REWORK[link] they talks about using a sharpie pen to restrict the amount of detail. This is a neat trick to force a more layout oriented approach rather than worry about the nitty gritty. You’ll find yourself asking  ‘where shall I place the login button?’ instead of ‘should the login button have rounded corners?’.

<div class="fit-img">
    <img src="/static/img/media/admino-mockup.png"/>
</div>

The original mockup for this project is above. Mockup can undergo several passes and revisions (even beyond the start of a project). When creating a mockup I try to first focus on structure.  What should the layout be? How will component fit together?
After the first pass, I’ll usually go back in and add more specifics (any user interaction, color ideas, etc).
The level of detail in mockup varies between projects. I’ll try to get a mockup to a point where it summarize the core ideas of a design but not bogged down with details (e.g. shadows on buttons, copy, etc).

Once I felt happy with the mockup. It was time to start coding...

That is all for this post. In the next part of the series, we’ll begin the process of turning the mockup into a functional site.

[1]: https://wrapbootstrap.com/theme/admino-fixed-width-admin-template-WB064S498?ref=cameron
[2]: http://wrapbootstrap.com/preview/WB064S498
[3]: http://en.wikipedia.org/wiki/Create,_read,_update_and_delete
