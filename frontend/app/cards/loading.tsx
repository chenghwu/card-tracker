import { MainLayout } from '@/components/layout/main-layout';
import { Skeleton } from '@/components/ui/skeleton';

export default function CardsLoading() {
  return (
    <MainLayout>
      <div className="space-y-8">
        <div className="flex items-center justify-between">
          <div>
            <Skeleton className="h-9 w-32 mb-2" />
            <Skeleton className="h-5 w-64" />
          </div>
          <Skeleton className="h-10 w-28" />
        </div>

        <div className="space-y-8">
          {[1, 2].map((section) => (
            <div key={section}>
              <Skeleton className="h-7 w-32 mb-4" />
              <div className="grid gap-4 sm:gap-6 grid-cols-1 sm:grid-cols-2 lg:grid-cols-3">
                {[1, 2, 3].map((card) => (
                  <div key={card} className="border rounded-lg overflow-hidden">
                    <Skeleton className="h-48 w-full" />
                    <div className="p-4 space-y-3">
                      <Skeleton className="h-6 w-3/4" />
                      <Skeleton className="h-4 w-1/2" />
                      <div className="space-y-2">
                        <Skeleton className="h-3 w-full" />
                        <Skeleton className="h-3 w-2/3" />
                      </div>
                      <Skeleton className="h-10 w-full" />
                    </div>
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </MainLayout>
  );
}
