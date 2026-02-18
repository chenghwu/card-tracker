'use client';

import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { CreditCard } from 'lucide-react';
import Link from 'next/link';

export default function LoginPage() {
  const handleGoogleSignIn = () => {
    // Real Google OAuth flow via django-allauth (server-side redirect).
    //
    // The backend's /accounts/google/login/ kicks off the Google consent screen.
    // After the user grants access, Google redirects back to the Django backend
    // callback URL, allauth logs the user in, and Django redirects to
    // /api/auth/google/done/ which mints JWT tokens and redirects the browser to
    // /auth/callback?access=TOKEN&refresh=REFRESH_TOKEN on the frontend.
    //
    // The `next` param tells allauth where to send the user after login; we rely
    // on the LOGIN_REDIRECT_URL setting instead, but it is passed for clarity.
    // NEXT_PUBLIC_BACKEND_URL is the Django root (no /api suffix).
    // Falls back to stripping /api from NEXT_PUBLIC_API_URL for backwards compat.
    const backendUrl =
      process.env.NEXT_PUBLIC_BACKEND_URL ||
      (process.env.NEXT_PUBLIC_API_URL
        ? process.env.NEXT_PUBLIC_API_URL.replace(/\/api\/?$/, '')
        : 'http://localhost:8000');

    // No ?next= param — allauth rejects cross-domain next URLs as unsafe.
    // LOGIN_REDIRECT_URL in Django settings handles the post-login redirect.
    window.location.href = `${backendUrl}/accounts/google/login/`;

    // ---------------------------------------------------------------------------
    // DEMO FALLBACK — Remove this block once Google OAuth credentials are set up.
    // To use the demo: comment out the window.location.href line above and
    // uncomment the lines below. The token expires 2026-02-18.
    // ---------------------------------------------------------------------------
    // console.log('Google sign in clicked - setting demo token (fallback)');
    // const demoToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzczOTU0MTEzLCJpYXQiOjE3NzEzNjIxMTMsImp0aSI6ImY5ZDI4Mjc2MmY3YTQwYjliZDFjNWJhZDc4NTk1N2NiIiwidXNlcl9pZCI6IjMifQ.I7j6O95Op4ShQ8cwmKIocaT3XRPCbp0_fKi__RYc2-M';
    // localStorage.setItem('access_token', demoToken);
    // window.location.href = '/dashboard';
  };

  const handleAppleSignIn = () => {
    // Apple OAuth is not yet configured — falls back to the demo token for now.
    // TODO: Wire up Apple OAuth the same way as Google once credentials are set up.
    console.log('Apple sign in clicked - setting demo token (Apple OAuth not yet configured)');

    // Remove this when Apple OAuth is configured.
    const demoToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzczOTU0MTEzLCJpYXQiOjE3NzEzNjIxMTMsImp0aSI6ImY5ZDI4Mjc2MmY3YTQwYjliZDFjNWJhZDc4NTk1N2NiIiwidXNlcl9pZCI6IjMifQ.I7j6O95Op4ShQ8cwmKIocaT3XRPCbp0_fKi__RYc2-M';

    localStorage.setItem('access_token', demoToken);
    window.location.href = '/dashboard';
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-gradient-to-b from-background to-muted">
      <Card className="w-full max-w-md">
        <CardHeader className="space-y-4 text-center">
          <div className="mx-auto flex h-12 w-12 items-center justify-center rounded-full bg-primary">
            <CreditCard className="h-6 w-6 text-primary-foreground" />
          </div>
          <CardTitle className="text-2xl">Welcome to Card Tracker</CardTitle>
          <CardDescription>
            Sign in to start tracking your credit card benefits
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <Button
            className="w-full"
            variant="outline"
            size="lg"
            onClick={handleGoogleSignIn}
          >
            <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24">
              <path
                d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
                fill="#4285F4"
              />
              <path
                d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
                fill="#34A853"
              />
              <path
                d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"
                fill="#FBBC05"
              />
              <path
                d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"
                fill="#EA4335"
              />
            </svg>
            Continue with Google
          </Button>

          <Button
            className="w-full"
            variant="outline"
            size="lg"
            onClick={handleAppleSignIn}
          >
            <svg className="mr-2 h-5 w-5" viewBox="0 0 24 24">
              <path
                d="M17.05 20.28c-.98.95-2.05.8-3.08.35-1.09-.46-2.09-.48-3.24 0-1.44.62-2.2.44-3.06-.35C2.79 15.25 3.51 7.59 9.05 7.31c1.35.07 2.29.74 3.08.8 1.18-.24 2.31-.93 3.57-.84 1.51.12 2.65.72 3.4 1.8-3.12 1.87-2.38 5.98.48 7.13-.57 1.5-1.31 2.99-2.54 4.09l.01-.01zM12.03 7.25c-.15-2.23 1.66-4.07 3.74-4.25.29 2.58-2.34 4.5-3.74 4.25z"
                fill="currentColor"
              />
            </svg>
            Continue with Apple
          </Button>

          <div className="relative">
            <div className="absolute inset-0 flex items-center">
              <span className="w-full border-t" />
            </div>
            <div className="relative flex justify-center text-xs uppercase">
              <span className="bg-background px-2 text-muted-foreground">
                Or
              </span>
            </div>
          </div>

          <div className="text-center text-sm text-muted-foreground">
            <Link href="/" className="underline underline-offset-4 hover:text-primary">
              Back to home
            </Link>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
