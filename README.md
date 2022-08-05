# Quick overview about solution - TwiJournal


Author: Paulo Rodrigues
email: paulorodriguesxv@gmail.com

## Overview

The Project aims to provide an example of Clean Architecture from Uncle Bob, using python and should be used only as an educational resource. The project is a simple application that allows you to create a new social media application called TwiJournal. TwiJournal is very similar to Twitter, but it has far fewer features.

TwiJournal only has two pages, the homepage and the user profile page, which are described below. Other data and actions are also detailed below.

This project is a simple example of how to use the Clean Architecture but it is not a complete solution and does not intend to be a source of truth.

We're open to suggestions and improvements.

## Project Structure

### Adapters
  1. **endpoints**
      Endpoints are the classes that handle the requests to the server. It could be a REST API, or a GraphQL API, or a websocket API. In this example, we use a REST API from fastapi. But it easy to change to Flask, or any other framework, even AWS lambdas.
      
      1. **fastapi**
      2. **Extending**: flask and another framework, lambdaserver, etc.

  2. **Gateway**
      Gateway is any component or layer that abstracts the communication with external services. Like database, cache, etc.
      Here we're using repository pattern to abstract the communication with the database.

      1. **SqlAlchemy**
           1. models
           2. repository
      2. **Extending**
        We could create a gateway to another services, MongoDB and other databases
   
### Use Cases / Business Rules

The software in this layer contains application specific business rules. It encapsulates and implements all of the use cases of the system. These use cases orchestrate the flow of data to and from the entities, and direct those entities to use their enterprise wide business rules to achieve the goals of the use case.

We do not expect changes in this layer to affect the entities. We also do not expect this layer to be affected by changes to externalities such as the database, the UI, or any of the common frameworks. This layer is isolated from such concerns.

We do, however, expect that changes to the operation of the application will affect the use-cases and therefore the software in this layer. If the details of a use-case change, then some code in this layer will certainly be affected.

Having this in mind, we can expect changes from FastAPI to Flask or SqlAlchemy to another framework doesn't affect the use-cases.

*USE CASE NEVER SHOULD ACCESS EXTERNAL SERVICES DIRECTLY OR BE FRAMEWORK DEPENDENT*

### Entities

Entities encapsulate Enterprise wide business rules. An entity can be an object with methods, or it can be a set of data structures and functions. It doesn’t matter so long as the entities could be used by many different applications in the enterprise.

Repository pattern is used here.


### Infrastructure

General infrastructure purpose


### Dependency Inversion and Dependency Injection

Here are some examples of Dependency Inversion and Dependency Injection using injector.
We choose to use injector because it is a lightweight and easy to use dependency injection library and it's framework independent.

Always as possible, use interfaces to define API contracts between components.

## Phase 1, coding

### Pages

**Homepage**

- The homepage, by default, will show a feed of posts (including reposts and quote posts), starting with the latest 10 posts. Older posts are loaded on-demand on chunks of 10 posts whenever the user scrolling reaches the bottom of the page
  
  -  This feautre implementation can be seen on the Feed API. Please see http://localhost:8000/docs for more info
  -  The following test use case is testing this feature:
  -  Tests
     -  test_should_see_only_ten_posts_when_load_feed
     
     
- There is a toggle switch "All / following" that allows you to switch between seeing all posts and just posts by those you follow. For both views, all kind of posts are expected on the feed (regular posts, reposts, and quote post).     
  -  This feautre implementation can be seen on the Feed API. Please see http://localhost:8000/docs for more info 
  -  Tests:
     -  test_should_see_only_followee_posts_when_load_feed

- New posts can be written from this page.
  - This feautre implementation can be seen on the Post API. Please see http://localhost:8000/docs for more info 
  - Tests
    - test_should_be_able_to_post_original_successfully
    - test_should_be_able_to_repost_successfully
    - test_should_be_able_to_quote_post_successfully

**User profile page**

- Shows data about the user:
    - Username
    - Date joined TwiJournal, formatted as such: "March 25, 2021" 
    - Number of followers
    - Number following
    - Count of number of posts the user has made (including reposts and quote posts)

    - This feautres implementation can be seen on the User API. Please see http://localhost:8000/docs for more info 
    - Endpoint: http://localhost:8000/users/{username}
    - Tests
      - test_new_user_is_created
        - **Date joined TwiJournal is created_at field**
        - **formatted as such: "March 25, 2021" -> should be done by the frontend, not the backend**

- Shows a feed of the posts the user has made (including reposts and quote posts), starting with the latest 5 posts. Older posts are loaded on-demand when the user clicks on a button at the bottom of the page labeled "show more".
    - This feautres implementation can be seen on the Post API. Please see http://localhost:8000/docs for more info 
    - Endpoint: http://localhost:8000/posts/{username}?page={page_number}
    - Tests
      - test_should_be_able_to_quote_post_successfully
      - test_should_allow_post_five_post_on_day
      - test_should_be_able_to_post_original_successfully
      - test_should_be_able_to_repost_successfully
      - test_should_be_able_to_quote_post_successfully

- Shows whether you follow the user or not
    - This feautres implementation can be seen on the User API. Please see http://localhost:8000/docs for more info 
    - Endpoint: http://localhost:8000/users/{username}
    - Tests
      - test_should_have_zero_followee_when_unfollow_someone
      - test_should_have_one_followee_when_follow_someone
      - test_should_have_one_follower_when_followed_by_someone

- Follow/unfollow actions:
    - This feautres implementation can be seen on the User API. Please see http://localhost:8000/docs for more info 
    - Endpoint: http://localhost:8000/users/{username}
      - You can follow the user by clicking "Follow" on their profile
        - test_should_have_one_followee_when_follow_someone
      - You can unfollow the user by clicking "Unfollow" on their profile
        - test_should_have_zero_followee_when_unfollow_someone

- New posts can be written from this page
    - This feautres implementation can be seen on the Post API. Please see http://localhost:8000/docs for more info 
    - Endpoint: http://localhost:8000/posts/{username}?page={page_number}
    - Tests
      - test_should_be_able_to_quote_post_successfully
      - test_should_allow_post_five_post_on_day
      - test_should_be_able_to_post_original_successfully
      - test_should_be_able_to_repost_successfully
      - test_should_be_able_to_quote_post_successfully
      - test_should_fail_when_max_size_text_overcome
      - test_should_allow_max_size_text_successfully
      - test_should_allow_post_five_post_on_day

### More Details

**Users**

- Only alphanumeric characters can be used for username
- Maximum 14 characters for username
- Do not build authentication
- Do not build CRUD for users
- When/if necessary to make your application function, you may hard-code the user. For example, you may need to do this to implement creating new posts, following, etc

This feautres implementation can be seen on the User API. Please see http://localhost:8000/docs for more info 
- Tests
  - test_should_fail_when_new_user_have_more_than_14_char
  - test_new_user_is_created (it was necessary to create a endpoint for user registration)

**Posts**

Posts are the equivalent of Twitter's tweets. They are text only, user generated content. Users can write original posts and interact with other users' posts by reposting or quote-posting. For this project, you should implement all three — original posts, reposts, and quote-posting

- A user is not allowed to post more than 5 posts in one day (including reposts and quote posts)
- Posts can have a maximum of 777 characters
- Users cannot update or delete their posts
- Reposting: Users can repost other users' posts (like Twitter Retweet)
- Quote-post: Users can repost other user's posts and leave a comment along with it (like Twitter Quote Tweet)

This feautres implementation can be seen on the Post API. Please see http://localhost:8000/docs for more info 
- Tests
  - test_should_be_able_to_quote_post_successfully
  - test_should_allow_post_five_post_on_day
  - test_should_be_able_to_post_original_successfully
  - test_should_be_able_to_repost_successfully
  - test_should_be_able_to_quote_post_successfully
  - test_should_fail_when_max_size_text_overcome
  - test_should_allow_max_size_text_successfully
  - test_should_allow_post_five_post_on_day

**Following**

- Users should be able to follow other users
- Users cannot follow themselves
- Following and unfollowing will be done only on the user profile page (frontend responsability)

This feautres implementation can be seen on the user API. Please see http://localhost:8000/docs for more info 
- Tests
  - test_should_fail_on_try_following_himself
  - test_should_have_one_follower_when_followed_by_someone
  - test_should_have_one_followee_when_follow_someone
  - test_should_have_zero_followee_when_unfollow_someone
  - test_should_have_followee_equal_two_when_follow_two_person

### Extra **feature: Search**

Only work on this extra feature if you have enough time to complete the required features and get through all three phases of the interview.

- Implement a search feature that allows users to efficiently search through all posts
- This search feature should not return reposts
- This search feature should return quote posts, but only if the search matches the additional text added (do **not** return matches from the original post that was quoted on top of)
- (For Phase 2) This search feature should return reply-to-posts

**`I did not work on that feature. But in case I had to work on it, I would choose something approach using Elasticsearch. But for sure that would be a service desacopled from this base TwiJournal backend`**




# Running it

The easiest way to run it is using docker. To do it, you should have docker and docker-compose installed on your machine. Access the TwiJournal project root folder and type:

```bash
  docker-compose up -d
```

This command will startup an MariaDB database instance and build and run the TwiJournal Api Server instance. 
By default some date will be seeded on the first time running:
  - Users: usera, userb, userc, userd, userf
  - Followers
  - Posts
  - Statistics

Insominia Rest Api Collection:
  Just import TwiJournal_Insomnia_Collection.json to your Insominia 

**To generate an access token for a given user, just access http://localhost:8000/docs and look for Seed Api**

**To know about Models, Payloads and Api documentation, see Swagger session of this readme**  

# Developer Guide

Requirements:
  - [Python 3.9](https://www.python.org/)
  - [Poetry](https://python-poetry.org/)

After downloading code, install poetry and execute `poetry install` inside project root directory to install all dependencies:

## Mainly architectural features
  - Clean Architecture approach 
  - REST Maturity level 3 - Hateoas 
  - FastAPI framework
  - Alembic for database migrations
## Environment variable

  Copy .env.template file to .env in the case do you not want to configure this variables in your operational system

 - `DATABASE_URL`=mysql+pymysql://mariadb:mariadb@127.0.0.1:3306/twijournal_db
 - `MAX_POSTS_PER_PAGE`: number of default posts displayed at user profile page
     - MAX_POSTS_PER_PAGE=5
 - `MAX_FEED_POSTS_PER_PAGE`: number of posts displayed by default at feed page
     - MAX_FEED_POSTS_PER_PAGE=10
 - `POST_URI`: base path used in hateoas contract for posts
     - POST_URI=http://localhost:8000/posts/
 - `FEED_URI`: base path used in hateoas contract for posts
     - FEED_URI=http://localhost:8000/feeds/
 - `USER_MAX_POST_PER_DAY`: user quota of post per day by user
     - USER_MAX_POST_PER_DAY=5
 - `PORT`=8000
  
## Migration

Database migration and seed is made by the first time TwiJournal run, but in case do you want to execute manually, just execute this command:

```bash
 alembic upgrade head
 ```
## Run server in developer mode

uvicorn twijournal.main:app --reload --loop asyncio 

## Swagger

The project documentation is based on OpenAPI. You can access TwiJournal project documentation [here](http://localhost:8000/docs)
## Generate token: 

It is necessary to generate a JWT Token to perform some operations. It should be necessary due to fact we need to know the user that is performing the operation, for example, the user that is creating a post. It's possible to use jwt.io using this payload

```json
 {
  "sub": "1234567890",
  "name": "John Doe",
  "username": "usera",
  "iat": 1516239022
}
```

This token should be passed as a Authorization Bearer token on given requests

Example:

Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwidXNlcm5hbWUiOiJnRjN0U3k2QVJHckNEIiwiaWF0IjoxNTE2MjM5MDIyfQ.mR0ljmSEjkV0bLUluYx24pfOANQ4vBuSU71MluSokr0


## Test and Coverage
pytest  --cov-report html:cov_html --cov=twijournal tests/

Actual coverage: 90%



# Planning

- Write down questions you have for the Product Manager about implementation.
  - This feature seems to be very similar to a comment feature. Is this understanding correct?
  - replying to a post should generate a new quote-post from the user who has replied the original post?
  - The comments that will be displayed at this new feed have to follow what kind of order? More relevants first, newers first, etc?
  - How much replies have to be displyed at first page view, I mean, how to set a order?
  - Will be possible to reply a reply?


- Write about how you would solve this problem in as much detail as possible. Write about all of the changes to database/front-end/api/etc that you expect. You should write down any assumptions you are making from any questions for the Product Manager that you previously mentioned.
   - It is not possible to set which changes or architectural path to follow because there are a few fundamental points opened here. But from a top-bottom view, we need a new mechanism to store data and link them with posts. It will be necessary to have a new API endpoint, basically CRUD operations related to these replies. For our project approuch it's mean to create a new external access (endpoint/controller), change post use case to include reply operations and create some news entities.


# Critique

In a real world, I would split this service in at least two others services. One would be responsable to deal with post creating operations and other only forread post operations, like some a CQRS systems does, because I believe that read operations will happen more frequently than post creation. So, the services could scale 

Maybe thinking about scalability, we could use a cloud provider and turn some endpoints int lambadas and use database as service. It's totally easy to implement in our project, basically we just need to create a new gateway layer to deal with lambadas as endpoints (today we have only rest_fastapi http endpoint).