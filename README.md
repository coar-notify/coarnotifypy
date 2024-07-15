# COAR Notify

TODO

## Adding a new model

1. Create a new module for the model in `coarnotify.models` (for example `coarnotify.models.announce_ingest`)
2. Create the new model class in the new module (for example, `AnnounceIngest`) and implement as needed
3. Add the new model to `coarnotify.models.__init__.py` so it can be imported from `coarnotify.models`
4. Add the new model to the factory list of models in `coarnotify.common.COARNotifyFactory.MODELS`
5. Create a fixture and fixture factory in `coarnotify.test.fixtures` (for example, `coarnotify.test.fixtures.announce_ingest`)
6. Add a unit test for the new model in `coarnotify.test.unit.test_models`, and confirm it works
7. Add an integration test for the new model in `coarnotify.test.integration.test_client`, and confirm it works