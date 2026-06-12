# React/TypeScript Best Practices

> Coding standards for React/TypeScript in Agentic SDLC projects.

---

## Code Style

```typescript
// Good — Typed, concise
interface Props {
  data: Item[];
  onSelect: (id: string) => void;
}

export const ItemList = ({ data, onSelect }: Props) => {
  return (
    <div className="space-y-2">
      {data.map(item => (
        <ItemRow key={item.id} data={item} onClick={() => onSelect(item.id)} />
      ))}
    </div>
  );
};

// Avoid — any types, verbose
export const ItemList = (props: any) => {
  return (
    <div>
      {props.data.map((item: any) => (
        <ItemRow key={item.id} data={item} onClick={() => props.onSelect(item.id)} />
      ))}
    </div>
  );
};
```

## Key Rules

- **TypeScript strict mode:** Always
- **Props interfaces:** Define explicitly
- **Hooks:** Use functional components + hooks
- **State management:** useState for local, Zustand/Context for global
- **Styling:** Tailwind utility classes (avoid custom CSS when possible)
- **API calls:** Separate service layer (api.ts)
- **Error boundaries:** Wrap critical components

## Project Structure

```
frontend/
├── src/
│   ├── components/    # React components
│   ├── services/      # API clients, WebSocket
│   ├── stores/        # State management
│   ├── types/         # TypeScript types
│   └── utils/         # Helpers
├── public/
└── vite.config.ts
```
