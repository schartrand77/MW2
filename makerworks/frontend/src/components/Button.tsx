import { ButtonHTMLAttributes } from 'react';
import classNames from 'classnames';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'destructive';
}

export default function Button({ variant = 'primary', ...props }: Props) {
  return <button className={classNames(variant)} {...props} />;
}
