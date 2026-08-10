#!/usr/bin/env python3
"""Add first-occurrence links to vocabulary terms in documentation."""

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Vocabulary: list of (term, target_path_relative_to_root)
VOCAB = []

def add_core(filename, forms):
    for form in forms:
        VOCAB.append((form, f"core-definitions/{filename}"))

def add_common(filename, forms):
    for form in forms:
        VOCAB.append((form, f"primitive-types/{filename}"))

def add_topic(filename, forms):
    for form in forms:
        VOCAB.append((form, f"topics/{filename}"))

# Core primitives (case-sensitive, capitalized)
add_core('alias.md', ['Aliases', 'Alias'])
add_core('app.md', ['Apps', 'App'])
add_core('channel.md', ['Channels', 'Channel'])
add_core('exonet.md', ['Exonets', 'Exonet'])
add_core('identity.md', ['Identities', 'Identity'])
add_core('link.md', ['Links', 'Link'])
add_core('local-swarm.md', ['Local Swarms', 'Local Swarm'])
add_core('node.md', ['Nodes', 'Node'])
add_core('object-id.md', ['Object IDs', 'Object ID'])
add_core('object-stream.md', ['Object Streams', 'Object Stream'])
add_core('object-type.md', ['Object Types', 'Object Type'])
add_core('object.md', ['Objects', 'Object'])
add_core('op.md', ['Operations', 'Operation', 'Ops', 'Op'])
add_core('protocol.md', ['Protocols', 'Protocol'])
add_core('query-string.md', ['Query Strings', 'Query String'])
add_core('query.md', ['Queries', 'Query'])
add_core('stamp.md', ['Stamps', 'Stamp'])
add_core('structure.md', ['Structures', 'Structure'])
add_core('swarm.md', ['Swarms', 'Swarm'])
add_core('user.md', ['Users', 'User'])

# Common types (lowercase)
add_common('ack.md', ['ack'])
add_common('bool.md', ['bool'])
add_common('eos.md', ['eos'])
add_common('error_message.md', ['error_message'])
add_common('identity.md', ['identity'])
add_common('int8.md', ['int8'])
add_common('int16.md', ['int16'])
add_common('int32.md', ['int32'])
add_common('int64.md', ['int64'])
add_common('nonce64.md', ['nonce64'])
add_common('object.md', ['object'])
add_common('object_id.sha256.md', ['object_id.sha256'])
add_common('string8.md', ['string8'])
add_common('string16.md', ['string16'])
add_common('string32.md', ['string32'])
add_common('string64.md', ['string64'])
add_common('time.md', ['time'])
add_common('uint8.md', ['uint8'])
add_common('uint16.md', ['uint16'])
add_common('uint32.md', ['uint32'])
add_common('uint64.md', ['uint64'])

# Topics
add_topic('app-routing.md', ['App Routing'])
add_topic('astral-ipc.md', ['Astral IPC'])
add_topic('op-modes.md', ['Op modes', 'Batch mode'])
add_topic('binary-encoding.md', ['Binary Encoding'])
add_topic('blueprints.md', ['Blueprints', 'Blueprint'])
add_topic('codec.md', ['Codec'])
add_topic('http-transport.md', ['HTTP Transport'])
add_topic('json-encoding.md', ['JSON Encoding'])
add_topic('network-architecture.md', ['Network Architecture'])
add_topic('node-claiming.md', ['Node Claiming'])
add_topic('node-setup.md', ['Node Setup'])
add_topic('text-encoding.md', ['Text Encoding'])
add_topic('ws-transport.md', ['WebSocket Transport', 'WebSocket transport'])


def is_lowercase_common_type(target):
    return target.startswith('primitive-types/')


def find_code_block_zones(lines):
    """Return set of line indices inside fenced code blocks (including fence lines)."""
    zones = set()
    in_fence = False
    for i, line in enumerate(lines):
        stripped = line.lstrip()
        if stripped.startswith('```') or stripped.startswith('~~~'):
            zones.add(i)
            in_fence = not in_fence
            continue
        if in_fence:
            zones.add(i)
    return zones


def is_heading(line):
    return line.lstrip().startswith('#')


def find_inline_code_spans(line):
    """Find inline code spans `text` and return list of (start, end, content).

    Uses simple single-backtick matching (CommonMark supports multi, but our docs
    only use single backticks). end is exclusive of the closing backtick + 1.
    """
    spans = []
    pos = 0
    while pos < len(line):
        if line[pos] == '`':
            close = line.find('`', pos + 1)
            if close > pos:
                spans.append((pos, close + 1, line[pos + 1:close]))
                pos = close + 1
            else:
                pos += 1
        else:
            pos += 1
    return spans


def find_existing_link_spans(line):
    """Return list of (start, end) spans for existing [text](url) links."""
    return [(m.start(), m.end()) for m in re.finditer(r'\[[^\]]*\]\([^)]*\)', line)]


def in_any_span(pos, spans):
    return any(s <= pos < e for s, e in spans)


def in_any_span_range(start, end, spans):
    return any(s <= start and end <= e for s, e in spans)


def compute_relative_path(from_dir, to_path):
    return os.path.relpath(to_path, from_dir).replace('\\', '/')


def collect_existing_link_targets(lines, code_zones, file_dir):
    """Map vocab target abs-path -> first line idx with an existing link to it."""
    vocab_targets = {str((ROOT / p).resolve()) for _, p in VOCAB}
    targets_seen = {}
    for i, line in enumerate(lines):
        if i in code_zones:
            continue
        for m in re.finditer(r'\[[^\]]*\]\(([^)]+)\)', line):
            url = m.group(1)
            url_no_frag = url.split('#', 1)[0]
            if not url_no_frag.endswith('.md'):
                continue
            try:
                target = (file_dir / url_no_frag).resolve()
            except Exception:
                continue
            target_str = str(target)
            if target_str in vocab_targets and target_str not in targets_seen:
                targets_seen[target_str] = i
    return targets_seen


def find_term_matches(line, term, is_lowercase, code_spans, link_spans):
    """Find all match candidates of `term` in `line`.

    Returns list of (start, end, original_text), where `original_text` is the
    text to wrap (e.g. "`term`" or "*term*" or "term"). Multi-char backtick spans
    that contain more than the term are excluded. Existing-link spans are
    excluded.
    """
    candidates = []
    term_esc = re.escape(term)

    # 1. Inline code span exactly equal to the term: linkable as `term`
    for s, e, content in code_spans:
        if content == term:
            if in_any_span(s, link_spans):
                continue
            candidates.append((s, e, line[s:e]))

    if not is_lowercase:
        # 2. Italic *term* (single asterisks, not part of **)
        for m in re.finditer(rf"(?<!\*)\*{term_esc}\*(?!\*)", line):
            start, end = m.start(), m.end()
            # Skip if inside any code span or existing link
            if in_any_span(start, [(s, e) for s, e, _ in code_spans]):
                continue
            if in_any_span(start, link_spans):
                continue
            candidates.append((start, end, m.group()))

        # 3. Plain term with non-word, non-formatting boundaries
        for m in re.finditer(rf"(?<![\w`*\-]){term_esc}(?![\w`*\-])", line):
            start, end = m.start(), m.end()
            if in_any_span(start, [(s, e) for s, e, _ in code_spans]):
                continue
            if in_any_span(start, link_spans):
                continue
            candidates.append((start, end, m.group()))

    candidates.sort(key=lambda x: x[0])
    return candidates


def process_file(file_path):
    rel_path = str(file_path.relative_to(ROOT)).replace('\\', '/')
    file_dir = file_path.parent

    with open(file_path) as f:
        original = f.read()
    lines = original.split('\n')

    code_zones = find_code_block_zones(lines)
    existing_targets = collect_existing_link_targets(lines, code_zones, file_dir)

    # Vocab relevant to this file: exclude self-links
    relevant_vocab = [(t, p) for t, p in VOCAB if p != rel_path]

    # Group vocab by target so all forms (singular/plural) share state
    by_target = {}
    for term, target in relevant_vocab:
        by_target.setdefault(target, []).append(term)

    edits_by_line = {}
    claimed = {}
    added_links = []

    # Process targets in deterministic order; longest-form first to handle
    # multi-word terms before their substrings.
    target_order = sorted(by_target.keys(),
                          key=lambda t: (-max(len(x) for x in by_target[t]), t))

    for target in target_order:
        abs_target = str((ROOT / target).resolve())
        if abs_target in existing_targets:
            continue

        terms = sorted(by_target[target], key=lambda t: -len(t))
        is_lc = is_lowercase_common_type(target)

        # Find earliest valid match across all forms of this target
        best = None  # (line_idx, start, end, orig, term)
        for line_idx, line in enumerate(lines):
            if line_idx in code_zones:
                continue
            if is_heading(line):
                continue

            code_spans = find_inline_code_spans(line)
            link_spans = find_existing_link_spans(line)
            line_claimed = claimed.get(line_idx, [])

            for term in terms:
                for start, end, orig in find_term_matches(
                        line, term, is_lc, code_spans, link_spans):
                    if any(cs <= start and end <= ce for cs, ce in line_claimed):
                        continue
                    if best is None or (line_idx, start) < (best[0], best[1]):
                        best = (line_idx, start, end, orig, term)
                    break  # earliest match for this term on this line

            if best is not None and best[0] < line_idx:
                # Already found a match on an earlier line; stop scanning further lines
                break

        if best is None:
            continue

        line_idx, start, end, orig, term = best
        rel_target = compute_relative_path(file_dir, ROOT / target)
        replacement = f"[{orig}]({rel_target})"
        edits_by_line.setdefault(line_idx, []).append((start, end, replacement))
        claimed.setdefault(line_idx, []).append((start, end))
        added_links.append((term, rel_target, replacement, orig))

    # Apply edits
    new_lines = list(lines)
    for line_idx, ed in edits_by_line.items():
        line = new_lines[line_idx]
        ed.sort(key=lambda x: -x[0])
        for start, end, replacement in ed:
            line = line[:start] + replacement + line[end:]
        new_lines[line_idx] = line

    new_content = '\n'.join(new_lines)

    if new_content != original:
        with open(file_path, 'w') as f:
            f.write(new_content)

    return added_links


def main():
    dirs = ['primitive-types', 'core-definitions', 'topics']
    all_added = {}
    for d in dirs:
        for f in sorted((ROOT / d).iterdir()):
            if f.suffix != '.md':
                continue
            if f.name == 'README.md':
                continue
            added = process_file(f)
            all_added[str(f.relative_to(ROOT))] = added

    total_files = 0
    total_links = 0
    for path in sorted(all_added.keys()):
        links = all_added[path]
        if links:
            total_files += 1
            total_links += len(links)
            print(f"\n{path}:")
            for term, target, _, _ in links:
                print(f"  +{term} → {target}")
    print(f"\n{total_files} files, {total_links} links added.")


if __name__ == '__main__':
    main()
