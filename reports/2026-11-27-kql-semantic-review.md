# KQL semantic review — 27 November 2026

Documentation-only source audit; pinned source links below. The permanent
candidate contract is the [detection result contract](../architecture/DETECTION-RESULT-CONTRACT.md).
DEC-0032, DEC-0003, CON-0001, CON-0014, CON-0015 and CON-0021 remain
binding. No runtime or reference-engine tests executed.

| ID | Source observation | Candidate correction or qualification |
|---|---|---|
| SEM-01 | [KqlValue](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/a94dda9cfd87c950b4996cffdb33f3d4c980b485/src/DeltaZulu.Kql/KqlValue.cs) uses CLR type/value equality and HashCode.Combine. | Keep representation equality separate from bound expression/grouping semantics and durable keys. |
| SEM-02 | Null factory accepts any non-null scalar symbol; default struct has no declared type; String rejects null while typed-null factory accepts string. | Validate declared surface and distinguish carrier null from language semantics. |
| SEM-03 | Dynamic accepts arbitrary object; CLR equality need not be structural or immutable. | No dynamic key support until qualified; snapshot supported values. |
| SEM-04 | [KqlTypes](https://github.com/DeltaZulu-OU/DeltaZulu.Kql/blob/a94dda9cfd87c950b4996cffdb33f3d4c980b485/src/DeltaZulu.Kql/KqlTypes.cs) normalizes declared types; real conversion flags long/ulong beyond 2^53 as Narrowed, including exactly representable values beyond that boundary. | Treat flag as conservative potential loss, not proof of actual rounding; test exactness and policy before changing normalization. |
| SEM-05 | [TumblingAggregateInput](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/TumblingAggregateInput.cs) requires nonblank string key and always supplies distinct bytes; [ResultKey](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Results/ResultKey.cs) also requires nonblank key. | Encode empty/null group coordinates unambiguously; explicit excluded distinct operand. |
| SEM-06 | [ExactDistinctAccumulator](https://github.com/DeltaZulu-OU/DeltaZulu.LocalStream/blob/b900684308248a83a08550e0d66a8c52adad62fd/src/DeltaZulu.LocalStream.Query/Operators/ExactDistinctAccumulator.cs) compares canonical bytes and enforces cardinality/byte limits. | Retain exact membership; upstream equivalence and inclusion policy require verification. |
| SEM-07 | [KustoQueryCompiler](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Application/Analytics/Translation/KustoQueryCompiler.cs) and [KustoQueryTranslator](https://github.com/DeltaZulu-OU/DeltaZulu.Platform/blob/d6b3a435466d57317e4c70a26948ea5d68075675/src/DeltaZulu.Platform.Application/Analytics/Translation/KustoQueryTranslator.cs) produce relational nodes using Kusto analysis and syntax dispatch. | Reuse qualified binding, not automatic stream equivalence; verify supported overloads and diagnostics. |
| SEM-08 | CON-0021 documents different SyntaxKind integers across supported versions. | No persisted enum ordinals; packed consumer test under C14, not merely recompilation. |

## Candidate conformance fixtures

| Fixture | Required evidence |
|---|---|
| Typed null, absent field, conversion failure, empty string | Distinct provenance; reference-confirmed predicate and aggregate behavior |
| Default carrier and unsupported symbol | Explicit rejection, no accidental typed value |
| Int/long comparison and promotion; 2^53 boundaries; signed/unsigned limits | Bound semantics, explicit loss policy; no unintended identity collapse |
| Decimal 1.0 and 1.00, signed zero | Equal canonical keys where bound grouping says equal |
| Real signed zero, NaN, infinities | Reference-confirmed semantics or explicit unsupported diagnostic |
| Case variants, whitespace, empty, Unicode composed/decomposed, malformed surrogate | Bound comparison and reversible encoding; no implicit normalization |
| Composite keys with delimiter-like values and differing arity | No framing collision |
| UTC tick difference, equivalent instant, unspecified DateTime, negative duration | Preserve precision and carrier constraints |
| GUID byte-order round trip | Stable encoding across hosts |
| Dynamic object order, array order and mutable values | Reject unsupported key or demonstrate equivalence and immutability |
| Count rows with excluded distinct operand; exact vs approximate function | Correct independent counts and explicit capability rejection |
| Distinct budget and forced digest collision | Explicit incomplete/failure; full equality comparison |
| Same key across partitions, process restart, culture and package versions | Identical canonical bytes under same bound policy |
| Unsupported syntax/function, invalid binding and runtime failure | Structured diagnostics; never silently report clean non-match |

Use independently derived KQL reference expectations and compare
supported stream and lake execution on identical typed evidence and
scope. Kusto.Language binding alone is not a runtime oracle; SQL
agreement alone is not proof of KQL conformance. No reference-engine
access or tests were performed in this audit. Exact supported operators,
canonical binary format, null/empty aggregate behavior and numerical
budgets remain open under the joint C06/C07 gate. No Accepted Decision
or product source changed.
