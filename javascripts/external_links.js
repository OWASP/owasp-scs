document$.subscribe(function () {
  const internalHosts = new Set([
    window.location.hostname,
    'scs.owasp.org',
    'www.scs.owasp.org',
    'localhost',
    '127.0.0.1'
  ]);

  document.querySelectorAll('a[href]').forEach(function (link) {
    let url;

    try {
      url = new URL(link.getAttribute('href'), window.location.href);
    } catch (_error) {
      return;
    }

    if (!['http:', 'https:'].includes(url.protocol) || internalHosts.has(url.hostname)) {
      return;
    }

    const rel = new Set(
      (link.getAttribute('rel') || '')
        .split(/\s+/)
        .filter(Boolean)
    );

    rel.add('noopener');
    rel.add('noreferrer');

    link.setAttribute('target', '_blank');
    link.setAttribute('rel', Array.from(rel).join(' '));
  });
});
