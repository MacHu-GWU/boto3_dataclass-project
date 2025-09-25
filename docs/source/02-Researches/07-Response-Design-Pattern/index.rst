.. _Response-Wrapper-Design-Pattern:

Response Wrapper Design Pattern
==============================================================================


Problem Statement
------------------------------------------------------------------------------
When working with boto3 clients, developers often need to convert raw dictionary responses from AWS APIs into more structured, type-safe dataclass objects. The core challenge is providing a seamless conversion layer that doesn't require users to memorize complex return types or import statements. Users can easily remember client method names (like ``iam_client.get_role``), but they struggle to recall the exact TypedDict response types (like ``GetRoleResponseTypeDef``) needed for proper type conversion.

The goal is to create an elegant interface that allows users to call native boto3 APIs and effortlessly transform the results into dataclass objects without breaking existing workflows or requiring extensive code changes.


Proposed Solutions
------------------------------------------------------------------------------
1. **Proxy Pattern Client**: Create an enhanced client wrapper that intercepts method calls and automatically returns dataclass objects instead of dictionaries. This provides the most seamless experience but requires implementing proxies for all client methods. Example:

.. code-block:: python

    # usage
    dc_iam_client = DataClassIAMClient(boto3.client("iam"))
    role = dc_iam_client.get_role(RoleName="test")  # return dataclass

2. **Decorator Pattern**: Add decorators to existing clients that inject dataclass conversion capabilities, creating parallel methods with suffix notation (e.g., get_role_dc()). This maintains backward compatibility while adding new functionality. Example:

.. code-block:: python

    # usage
    dc_iam_client = dataclass_enhanced(boto3.client("iam"))
    role = dc_iam_client.get_role_dc(RoleName="test")  # dc suffix method returns dataclass

3. **Context Manager**: Use with statements to temporarily enable dataclass mode for specific code blocks. This provides clear conversion scope but requires additional syntax overhead. Example:

.. code-block:: python

    with dataclass_mode(client) as dc_client:
        role = dc_client.get_role(RoleName="test")

4. **Method Chaining**: Enable fluent interface by adding .to_dataclass() methods to response objects. This offers the most concise syntax but requires monkey-patching or response wrapping. Example:

.. code-block:: python

    role = client.get_role(RoleName="test").to_dataclass()

5. **Factory Function Pattern**: Provide factory functions that accept both the client and method parameters, handling the conversion internally. This approach requires passing the client as a parameter but offers maximum flexibility. Example:

.. code-block:: python

    role = caster.get_role(client.get_role(RoleName="test"))


Selected Approach: Factory Function Pattern
------------------------------------------------------------------------------
After careful consideration, we chose the factory function pattern for its optimal balance of simplicity, performance, and maintainability. This approach has minimal code intrusion, requires no complex proxy implementations, and provides the most straightforward user experience. It's the most sustainable long-term solution that preserves existing boto3 workflows while adding powerful type-safe conversion capabilities.
