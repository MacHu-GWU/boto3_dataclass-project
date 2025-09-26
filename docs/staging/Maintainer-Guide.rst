Automatic Code Generation from boto3-stubs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Rather than manually maintaining AWS service models, boto3-dataclasses **automatically generates all dataclasses by parsing boto3-stubs TypedDict definitions**. This approach provides several key advantages:

- **Always up-to-date**: Generated directly from the same type definitions used by boto3 itself
- **Complete coverage**: Supports all AWS services with their full API surface
- **Type safety guaranteed**: Inherits the same type annotations used by boto3-stubs, ensuring perfect IDE support and mypy compatibility
- **Zero maintenance overhead**: New AWS features and API changes are automatically reflected when you regenerate

The generation process uses Python's AST (Abstract Syntax Tree) to parse `.pyi` stub files, extracting TypedDict definitions and transforming them into equivalent dataclasses with lazy-loading properties. This means every `DescribeInstancesResponseTypeDef` becomes a `DescribeInstancesResponse` dataclass with identical structure but superior ergonomics.


Core Design Philosophy
------------------------------------------------------------------------------
boto3-dataclasses operates on the principle that **AWS APIs return well-formed data that doesn't need validation**—it needs better access patterns. By wrapping responses in lazy-loading dataclasses, you get clean, Pythonic access to your data without the computational overhead of eager validation or transformation. The library acts as a thin, type-safe interface layer that makes AWS responses feel like native Python objects while preserving their original structure and performance characteristics.


Builder Architecture
------------------------------------------------------------------------------
This library provides comprehensive dataclass coverage for all 414 AWS services, resulting in approximately 1.9 million lines of generated code with a total size of ~70MB. Due to this massive scale, it's impractical to require users to install the entire library at once—most users only need a subset of AWS services for their specific use cases.

To address this challenge, boto3-dataclasses employs a **modular builder architecture** similar to Bootstrap's approach, allowing users to selectively install only the AWS services they need. This architecture enables the generation and publication of 400+ individual packages from a single codebase.

The builder system works by:

- **Modular Code Generation**: Each AWS service is generated into its own isolated subdirectory
- **Independent Package Structure**: Each subdirectory simulates a complete Python package with its own setup files and dependencies
- **Automated Publishing Pipeline**: The builder orchestrates the creation and publication of individual packages to PyPI
- **Selective Installation**: Users can install specific services (e.g., ``pip install boto3-dataclass[ec2]``) rather than the entire ecosystem

This approach significantly reduces installation overhead while maintaining the convenience of a unified development and maintenance workflow.