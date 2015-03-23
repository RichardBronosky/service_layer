####################
Mobile Services Layer
####################

A lightweight, containerized API aggregator using only Python, Redis, and S3

------------

Overview
--------

If you've ever made a mobile app for a company that claims to have an API, you understand the difference between an API that was designed for mobile consumption and one that was not.

Key Challenges faced by mobile developers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Unnecessary authentication/authorization to retrieve non-sensitive data
#. Overly verbose output
#. Requiring multiple round trips to get all data facets
#. Requiring multiple APIs (often from multiple providers)
#. Pagination inconsistent with the app's requirements
#. Post-processing required to apply business rules
#. Slow delivery (often caused by realtime searching or computation)

All of this work is done in concert on thousands of slow, memory constrained devices on slow networks (and implemented in a different language for each mobile platform). It's truly insane. But, no one wants to change their API, nor do they want to pay you to host another API. So what's the solution? The one I've come up with is a lightweight API aggregator. It's containerized (using Docker) and uses Amazon S3 for storage and delivery. It's just Python and Redis. It doesn't even require a web server because there is no request-time computation.



Process Flow
~~~~~~~~~~~~

.. image:: http://i.imgur.com/458tEAD.png
    :width: 554px
    :align: center
    :height: 294px
    :alt: Process Flow Chart
    :target: http://i.imgur.com/458tEAD.png

Usage
~~~~~

#. Modify ``celeryconfig.py`` to point to your Redis server
#. Define a ``config.yml`` file. (sample.yml has been provided)
#. Define a parser. (a Python function that takes a string as an argument and returns a modified string.)
#. Add AWS credentials
#. Use the included tools to start the workers, flower and celerybeat


Tools included in the project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``msl_worker``

   -  Starts a Celery worker pool

-  ``msl_beat``

   -  Starts a Celery worker pool with Celerybeat active

-  ``msl_flower``

   -  Starts a Celery monitoring and managing web app

