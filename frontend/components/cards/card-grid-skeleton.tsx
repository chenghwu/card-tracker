import { Card, CardContent, CardHeader } from '@/components/ui/card';
import { Skeleton } from '@/components/ui/skeleton';

export function CardGridSkeleton() {
  return (
    <div className="space-y-8">
      {[1, 2].map((section) => (
        <div key={section}>
          <Skeleton className="h-7 w-32 mb-4" />
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map((card) => (
              <Card key={card} className="overflow-hidden">
                <CardHeader className="p-0">
                  <Skeleton className="h-48 w-full rounded-none" />
                </CardHeader>
                <CardContent className="p-4">
                  <Skeleton className="h-6 w-3/4 mb-2" />
                  <Skeleton className="h-4 w-1/2 mb-4" />
                  <div className="space-y-2">
                    <Skeleton className="h-3 w-full" />
                    <Skeleton className="h-3 w-2/3" />
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
