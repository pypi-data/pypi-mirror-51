=====
Usage
=====

To use pyoadr-ven in a project::

    import pyoadr_ven

This will import the OpenAdrVENAgent class.

Register VEN
------------
If you don't have a `ven_id`, you will need to register the VEN with the vtn.
You will need to Initialize the agent with a `ven_name` and `send_registration=True`.

.. code-block:: python

    agent =  OpenADRVenAgent(
            ven_name-"name_of_ven",
            send_registration=True,
            vtn_id="vtn_id",
            vtn_address="http://openadr-vtn-server.local",
            security_level="standard",
            poll_interval_secs=15,
            log_xml=True,
            opt_in_timeout_secs=3,
            opt_in_default_decision="optIn",
            request_events_on_startup=True,
            report_parameters={},
            client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
            vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
        )


Pre-Registered VEN
------------------
If you already know the `ven_id`, initialize an `OpenAdrVENAgent` with:

.. code-block:: python

    agent =  OpenADRVenAgent(
            ven_id="ven_id",
            vtn_id="vtn_id",
            vtn_address="http://openadr-vtn-server.local",
            security_level="standard",
            poll_interval_secs=15,
            log_xml=True,
            opt_in_timeout_secs=3,
            opt_in_default_decision="optIn",
            request_events_on_startup=True,
            report_parameters={},
            client_pem_bundle="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/client.pem",
            vtn_ca_cert="/home/peter/carboncoop/hems/docker/data/carboncoop-hems-shared-data/ca.crt",
        )

The first thing you are likely to want to do is get all of the existing events that are on the VTN.

.. code-block:: python

    agent.send_oadr_request_event()

This will return all of the events that are on the server and adds them to the agent's cache.
This should be done once.

Then, in a long running loop, run:

.. code-block:: python

    agent.run_main_processes()

