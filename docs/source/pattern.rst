Implementing a custom pattern
=============================

For many implementations you will be able to use the default pattern objects supplied by this library for your needs.

If your notifications have additional requirements, such as service-specific validation rules, or additional required
or optional fields, you can create your own pattern classes by subclassing the base pattern classes.

Adding a simple field
---------------------

Suppose we want to add a field to an ``AnnounceEndorsement`` pattern to indicate a "time to live" for the endorsement.
It doesn't really matter what this means, but lets suppose it's the number of days for which the endorsement record
is guaranteed to be available at the given identifier.

We would extend the :py:class:`AnnounceEndorsement` class like this:

.. code-block:: python

    from coarnotify.patterns import AnnounceEndorsement

    class AnnounceEndorsementWithTTL(AnnounceEndorsement):

        @property
        def ttl(self):
            return self.get_property('ttl')

        @ttl.setter
        def ttl(self, value):
            self.set_property('ttl', value)

Now any Announce Endorsement notification which contains a ``ttl`` field can be read and written using this object

Extending the validation
------------------------

We have added a custom field to the pattern in the previous section.  Now we want to validate that field to be
sure that it contains a positive integer.

There are two ways to approach this.  The simple way is for us to hard-code our validation:

.. code-block:: python

    from coarnotify.patterns import AnnounceEndorsement

    class AnnounceEndorsementWithTTL(AnnounceEndorsement):

        @property
        def ttl(self):
            return self.get_property('ttl')

        @ttl.setter
        def ttl(self, value):
            if not isinstance(value, int) or value < 0:
                raise ValueError('ttl must be a positive integer')
            self.set_property('ttl', value)

        def validate(self):
            # ask the superclass to do its own validation first, and catch
            # and keep any exceptions it raises to add to
            ve = ValidationError()
            try:
                super(AnnounceEndorsementItem, self).validate()
            except ValidationError as superve:
                ve = superve

            # now add our custom validation
            if not isinstance(self.ttl, int) or self.ttl < 0:
                ve.add_error('ttl', 'ttl must be a positive integer')

            if ve.has_errors():
                raise ve
            return True

There is a more formal (and verbose) way to do this, in line with how the library is designed.  This involves creating a custom validator
and adding it to the validation ruleset for the pattern.  Whether you take this approach depends on the extent to which
the validators you need are reused or shared across custom patterns.

.. code-block:: python

    from coarnotify.core.notify import VALIDATORS
    from coarnotify.patterns import AnnounceEndorsement
    from coarnotify.validation import Validator, ValidationError

    # create a validation function to check that a value is a positive integer
    def positive_integer(obj, x):
        if isinstance(x, int) and x > 0:
            return True
        raise ValueError("value must be a positive integer")

    # create a custom validation ruleset with the new rule
    RULES = VALIDATORS.rules()
    RULES['ttl'] = {"default": positive_integer}
    CUSTOM_VALIDATOR = Validator(rules=RULES)

    class AnnounceEndorsementWithTTL(AnnounceEndorsement):
            def __init__(self, stream: Union[ActivityStream, dict] = None,
                 validate_stream_on_construct=True,
                 validate_properties=True,
                 validators=None,
                 validation_context=None,
                 properties_by_reference=True):

                # force override the default validator and kick construction up to the superclass
                validators = CUSTOM_VALIDATOR
                super(AnnounceEndorsement, self).__init__(stream=stream,
                                                    validate_stream_on_construct=validate_stream_on_construct,
                                                    validate_properties=validate_properties,
                                                    validators=validators,
                                                    validation_context=validation_context,
                                                    properties_by_reference=properties_by_reference)

        @property
        def ttl(self):
            return self.get_property('ttl')

        @ttl.setter
        def ttl(self, value):
            self.set_property('ttl', value)

        def validate(self):
            # ask the superclass to do its own validation first, and catch
            # and keep any exceptions it raises to add to
            ve = ValidationError()
            try:
                super(AnnounceEndorsementItem, self).validate()
            except ValidationError as superve:
                ve = superve

            # now add our custom validation
            self.required_and_validate(ve, "ttl", self.ttl)

            if ve.has_errors():
                raise ve
            return True

Adding a complex/nested field
-----------------------------

Sometimes we want to customise fields that are not in the top level of the pattern, but nested in one of the
pattern parts.  In order to do that we can override the pattern part with a custom implementation, and then we must
wire in the custom part to the appropriate accessor on the pattern object.

For example, to add a custom ``object`` to our ``AnnounceEndorsement`` pattern, we would do the following:

First create our custom object, exteding ``NotifyObject``, which has a custom field imaginatively called ``custom_field``:

.. code-block:: python

    class AnnounceEndorsementObject(NotifyObject):
        @property
        def custom_field(self):
            return self.get_property('custom_field')

        @custom_field.setter
        def custom_field(self, value):
            self.set_property('custom_field', value)

Now we want it so when you call ``AnnounceEndorsement.object`` you get an instance of our custom object, not the
default ``NotifyObject``.  We do this by overriding the ``object`` property on the ``AnnounceEndorsement`` pattern:

.. code-block:: python

    from coarnotify.patterns import AnnounceEndorsement

    class AnnounceEndorsementWithCustomObject(AnnounceEndorsement):
        @property
        def object(self):
            obj = self.get_property(NotifyProperties.OBJECT)
            if obj is not None:
                return AnnounceEndorsementObject(obj,
                                  validate_stream_on_construct=False,
                                  validate_properties=self.validate_properties,
                                  validators=self.validators,
                                  validation_context=NotifyProperties.OBJECT,
                                  properties_by_reference=self._properties_by_reference)
            return None

Now when we access the ``object`` property on an ``AnnounceEndorsementWithCustomObject`` instance, we get an instance of
``AnnounceEndorsementObject``.