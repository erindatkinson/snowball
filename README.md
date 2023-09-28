# Snowball

A discord bot to enable a shared, sisyphean task of "number go up"

![](assets/crystal-ball-4006971_1920.jpg)
_Image by [Jill Wellington][image-credit]_

> _"Then if the countess is Sisyphus," Daisy concluded, "I suppose we're..."
> "The boulder," Lady Westcliff said succinctly._
>
> -Lisa Kleypas, It Happened One Autumn 

## Installation

### Requisites

* Python 3.8+
* Docker + docker-compose
* If you plan to run this on your own:
    * [Set up discord bot account][discord-bot]
    * :warning: This, again, is only if you intend to host the bot yourself.
* Pipenv
    * Install pipenv `pip install pipenv`
    * Run `pipenv install`
* Configure your .snowball.conf file
    * An example [.snowball.conf.example](./.snowball.conf.example) has been provided with the expected configuration variables.
    * (you likely won't need to change the permissions_integer)

## Building

The bot is currently set up to run in a docker container for your convenience, but isn't required to run if you'd rather set up a service with it. These commands all assume you'll be running in the container.

*  Run `make build`

### Initializing locally

* Run `make run` to start the container in docker-compose

## Bot Usage

The premise of the bot interaction is a shared channel of people trying to alternate counting to the highest they can.

chat example:

```
@Snowball[bot] (11:00:00) Hello from Snowball bot.
I just restarted, your last valid count was 0

@JannaBNana (11:00:45) 1
✅

@MertinsMcHuman (11:12:05) 2
✅

@ASpigotOfSpanners(11:12:05) 2
🌨

@ASpigotOfSpanners (11:13:30) _3 _2 * 3 -
✅

@JannaBNana (11:14) 5
❎

@Snowball[bot] (11:14) The cycle begins again

@MertinsMcHuman (11:15) 1
✅

@MertinsMcHuman (11:15) 2
🎭

@Snowball[bot] (11:15) A counting so nice, you made it twice?
```

### Counting

#### Valid countings:

* Message that is just an integer of the expected next count
    * eg. (1, 2, 3, 4, etc.)
* Reverse Polish Notation math that resolves to the expected next count
  * This is just shimmed out to the linux `dc` [desk calculator][desk-calculator], so any math that is valid for this is valid for snowball

#### Invalid countings:

* Message that is just an integer not of the expected next count
* Reverse Polish Notation math that does not resolves to the expected next count

#### Ignored messaged:

* Any message that doesn't start with either a digit or a `_` (dc uses `_`` for negative numbers)

### Reactions

* ✅: You made the correct count, the count has been increased
* 🌨: You tried to count too close to someone else and the bot could not acquire the mutex lock, it's okay to try again (likely with the next expected count after the other person got their count in)
* 🎭: You tried to count twice in a row, that's not a breaking no-no, but it IS a no-no, let other people have their turn
* ❎: Unfortunately you did not make the correct count, the count for your server has been reset to zero and the sisyphean ordeal must begin anew.

💜


[image-credit]: https://pixabay.com/users/jillwellington-334088/
[desk-calculator]: https://www.gnu.org/software/bc/manual/dc-1.05/html_mono/dc.html#SEC1
[discord-bot]: https://discordpy.readthedocs.io/en/latest/discord.html
