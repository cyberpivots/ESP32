export const TRANSCRIPT_FIRST_EVIDENCE_NOTE =
  "Transcript-first fixture evidence; screenshots and UI snapshots corroborate only.";

export function describeProof(label: string): string {
  return `${label}: ${TRANSCRIPT_FIRST_EVIDENCE_NOTE}`;
}
