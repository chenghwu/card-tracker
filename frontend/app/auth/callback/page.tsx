'use client';

import { Suspense, useEffect, useState } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { CreditCard, Loader2 } from 'lucide-react';

/**
 * OAuth Callback Page — /auth/callback
 *
 * After the Django backend completes the Google OAuth flow it redirects here
 * with JWT tokens as query parameters:
 *
 *   /auth/callback?access=ACCESS_TOKEN&refresh=REFRESH_TOKEN
 *
 * This page:
 *   1. Reads `access` and `refresh` from the URL search params.
 *   2. Stores them in localStorage under `access_token` and `refresh_token`.
 *   3. Redirects to /dashboard.
 *
 * If the tokens are missing (e.g. OAuth was denied or the URL is wrong) the
 * user is redirected back to /login with an error flag.
 *
 * Note: useSearchParams() requires a Suspense boundary when used in a page
 * component during static generation. The inner component is isolated so the
 * Suspense wrapper can be placed at the page level.
 */

function CallbackHandler() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const [status, setStatus] = useState<'loading' | 'error'>('loading');

  useEffect(() => {
    const access = searchParams.get('access');
    const refresh = searchParams.get('refresh');

    if (access && refresh) {
      // Store JWT tokens for use by the rest of the app
      localStorage.setItem('access_token', access);
      localStorage.setItem('refresh_token', refresh);

      // Navigate to the dashboard — replace the callback URL so the user
      // can't navigate back to this page with stale tokens in the URL.
      router.replace('/dashboard');
    } else {
      // Tokens not present — something went wrong with the OAuth flow.
      setStatus('error');
      router.replace('/login?error=oauth_failed');
    }
  }, [router, searchParams]);

  return (
    <>
      {status === 'loading' && (
        <>
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
          <p className="text-sm text-muted-foreground">Signing you in...</p>
        </>
      )}

      {status === 'error' && (
        <p className="text-sm text-destructive">
          Sign-in failed. Redirecting to login...
        </p>
      )}
    </>
  );
}

export default function AuthCallbackPage() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 bg-gradient-to-b from-background to-muted">
      <div className="flex h-12 w-12 items-center justify-center rounded-full bg-primary">
        <CreditCard className="h-6 w-6 text-primary-foreground" />
      </div>

      <Suspense
        fallback={
          <Loader2 className="h-8 w-8 animate-spin text-muted-foreground" />
        }
      >
        <CallbackHandler />
      </Suspense>
    </div>
  );
}
