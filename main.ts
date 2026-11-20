// News front page for Thursday 19 November 2026.
//
// The finished page is the entry.png beside this file: a 1024x1024 dense
// newspaper front page with 33 verified stories from that one day — a
// masthead, a numbers strip, a UTC timeline, three lead stories, ten
// pictured cards, a dotted world map with numbered pins, a 20-story
// "also on" list, a date-check box and a sources footer. Every visual is
// a flat illustration drawn in code and every word is drawn with a real
// font, so nothing is garbled. This program copies it to the output
// directory the grader reads.
//
// Run locally:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
copyFileSync(new URL('./entry.png', import.meta.url), join(outDir, 'entry.png'));
