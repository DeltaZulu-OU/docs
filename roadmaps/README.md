# Roadmaps

[**Consolidated execution roadmap**](CONSISTENCY-CORRECTNESS-ROADMAP.md) is the sole active work table. It has one work-item ID per row, priority, affected projects, status, acceptance criterion and decision boundary.

## Historical imports (read-only planning evidence)

These six files retain the original detailed milestone descriptions, statuses and review dates. Their original 2026-11-16 dates are historical, not pending active reviews. The 2026-11-25 reconciliation captured surviving topic groups; it did not establish current implementation status or approve stale priorities. Use the consolidated table for active work.

| Historical plan | Consolidated work |
|---|---|
| [Agent migration](DeltaZulu.Agent-ROADMAP.md) | C12, C05, C10, C08 |
| [Agent controller](DeltaZulu.Agent-DZAGENTCTL_CONTROLLER_ROADMAP.md) | C13 |
| [Forward](DeltaZulu.Forward-ROADMAP.md) | C03, C05, C14 |
| [LogCluster](DeltaZulu.LogCluster-ROADMAP.md) | C15 |
| [Platform](DeltaZulu.Platform-ROADMAP.md) | C03, C05–C07, C10, C11, C16, C17 |
| [Agent management](DeltaZulu.Platform-AGENT_MANAGEMENT_ROADMAP.md) | C17, C04, C16 |

Proton-specific tasks are retired under DEC-0033. Scheduled detection is deferred under DEC-0026. Do not revive direct Quack/Proton Agent output or dual-dialect compilation as target commitments. Preserve non-engine-specific requirements, including query safety and agent management, as candidates until verified.

Historical relative references to files not migrated here are not current links. Known relocated ADR/roadmap links have been repaired; missing originals must be recovered from the origin repository's history rather than guessed.

The no-fallback Forward contract remains in the historical Forward plan and DEC-0022's explicit fixture-only NDJSON boundary.
