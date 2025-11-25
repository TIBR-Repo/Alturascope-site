import React from "react";

type Props = {
  title: string;
  tagline: string;
  bullets: string[];
  bestFor?: string;
  sla?: string;
  outcomes?: string[];
  ctaLabel: string;
  ctaHref: string;
};

export default function ServiceCard({
  title,
  tagline,
  bullets,
  bestFor,
  sla,
  outcomes,
  ctaLabel,
  ctaHref,
}: Props) {
  return (
    <div className="rounded-2xl border border-gray-200 p-6 shadow-sm hover:shadow-md transition-shadow bg-white hover:border-accent">
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="mt-1 text-gray-700">{tagline}</p>

      <div className="mt-4">
        <h4 className="font-medium">Highlights</h4>
        <ul className="mt-2 list-disc pl-6 space-y-1 text-gray-800">
          {bullets.map((b, i) => (
            <li key={i}>{b}</li>
          ))}
        </ul>
      </div>

      {sla && (
        <p className="mt-4">
          <span className="font-medium">SLA: </span>
          {sla}
        </p>
      )}

      {bestFor && (
        <p className="mt-2">
          <span className="font-medium">Best for: </span>
          {bestFor}
        </p>
      )}

      {outcomes && outcomes.length > 0 && (
        <div className="mt-3">
          <h4 className="font-medium">Outcomes</h4>
          <ul className="mt-2 list-disc pl-6 space-y-1 text-gray-800">
            {outcomes.map((o, i) => (
              <li key={i}>{o}</li>
            ))}
          </ul>
        </div>
      )}

      <div className="mt-6">
        <a
          href={ctaHref}
          className="inline-flex items-center rounded-xl border border-accent text-primary px-4 py-2 text-sm font-medium transition-colors hover:bg-accent/10 active:bg-accent active:text-white"
        >
          {ctaLabel}
        </a>
      </div>
    </div>
  );
}



