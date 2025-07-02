import Link from 'next/link'
import Image from 'next/image'

export default function NotFound() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center">
      <div className="text-center">
        <Image
          src="/icon.png"
          alt="Logo"
          width={200}
          height={200}
          className="mx-auto mb-8"
        />
        <h1 className="text-4xl font-bold mb-4">404</h1>
        <p className="text-xl mb-6">There is no such page</p>
        <Link
          href="/"
          className="text-blue-600 hover:text-blue-800 underline"
        >
          Return to Home Page
        </Link>
      </div>
    </div>
  )
}
